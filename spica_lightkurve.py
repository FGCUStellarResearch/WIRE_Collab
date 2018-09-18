#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""
Code for playing around with the Lightkurve package to create lightcurves
for Spica based on C6 (K2ID: 212573842) and C17 (K2ID: 200213067) data.
Mostly follows the guide "How to use lightkurve for asteroseismology?" :
http://lightkurve.keplerscience.org/tutorials/2.09-how-to-use-lightkurve-for-asteroseismology.html 

Static Parameters:
    __C6_ID__ (int)         :   Spica C6 EPIC ID TODO: change to str?
    __C17_ID__ (int)        :   Spica C17 EPIC ID TODO: change to str?
    __output_folder__ (str) :   Location of output data

TODO:   Consider creating a Jupyter Notebook for this exercise.
NOTE:   MAST's K2 Data Search has an issue that prevents C17 from showing up
        when you enter "Spica"; the API will recognize the common name.
        Using the above listed EPIC IDs will get you the Spica data for the 
        respective campaigns.

Created 17 Sept 2018

.. codeauthor:: Lindsey Carboneau
"""

from lightkurve import KeplerTargetPixelFile as tpf
import matplotlib.pyplot as plt 
import numpy as np 
import os
from lightkurve import log
log.setLevel('ERROR')

# for use in debugging - blocks further execution until the plot/figure is displayed and manually closed by user
# plt.show(block=True)

# set up steps
__C6_ID__ = 212573842
__C17_ID__ = 200213067
if not os.path.isdir("toutput"):
    os.mkdir('toutput')
__output_folder__ = "./toutput/"

# download the Target Pixel File for the target
c6_tpf = tpf.from_archive(__C6_ID__, campaign=6)
c17_tpf = tpf.from_archive(__C17_ID__, campaign=17)

# save the target aperture, using the default pipeline aperture
c6_tpf.plot(scale='log', aperture_mask=c6_tpf.pipeline_mask)
plt.savefig(__output_folder__+'c6_tpf_aperture.png', bbox_inches='tight')
plt.close()

c17_tpf.plot(scale='log', aperture_mask=c17_tpf.pipeline_mask)
plt.savefig(__output_folder__+'c17_tpf_aperture.png', bbox_inches='tight')
plt.close()
# TODO: add ability to define our own aperture / use the interactive aperture tool (CoolStars20 team)
# TODO: create a function to create and save plots; code is reused frequently, so it will increase readability


# create raw lightcurves using SAP
c6_lc = c6_tpf.to_lightcurve().normalize().remove_nans().remove_outliers().fill_gaps()
c6_lc.plot()
plt.savefig(__output_folder__+'c6_lc_sap.png', bbox_inches='tight')
plt.close()

c17_lc = c17_tpf.to_lightcurve().normalize().remove_nans().remove_outliers().fill_gaps()
c17_lc.plot()
plt.savefig(__output_folder__+'c17_lc_sap.png', bbox_inches='tight')
plt.close()


# apply a 10 chunk SFF correction to the lightcurve
# NOTE: 'windows=10' is the example given for the SFF correction in the asteroseismology tutorial; using as a baseline
# NOTE: on my Windows computer, lightkurve.correct() throws an IndexError for all window sizes
# c6_clc = c6_lc.correct(windows=10).remove_outliers().fill_gaps()
# c6_clc.plot()
# plt.savefig(__output_folder__+'c6_clc_SFF_10.png', bbox_inches='tight')
# plt.close()

# c17_clc = c17_lc.correct(windows=10).remove_outliers().fill_gaps()
# c17_clc.plot()
# plt.savefig(__output_folder__+'c17_clc_SFF_10.png', bbox_inches='tight')
# plt.close()


# plot a periodogram for each of the corrected lightcurves
# TODO: when the lightcurve correction is working, this should plot the corrected and not the raw
c6_period = c6_lc.periodogram()
c6_period.plot(c='k')
plt.savefig(__output_folder__+'c6_raw_period.png', bbox_inches='tight')
plt.close()

c17_period = c17_lc.periodogram()
c17_period.plot(c='k')
plt.savefig(__output_folder__+'c17_raw_period.png', bbox_inches='tight')
plt.close()