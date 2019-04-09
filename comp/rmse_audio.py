#!/usr/bin/env python3

# =============================================================================
# Developer : Shashank Sharma(shashankrnr32@gmail.com)
# License : MIT License
# Year : 2019
# =============================================================================
# =============================================================================
# Description:
#     Plot Spectrum of a .wav file
# =============================================================================

import argparse
import matplotlib.pyplot as plot
import Utilities as util
import numpy as np
import sys
import math
from sklearn.metrics import mean_squared_error
def highestPowerof2(n): 
  
    p = int(math.log(n, 2)); 
    return int(pow(2, p));  

parser = argparse.ArgumentParser(description = 'Plot Frequency Spectrum of a .wav file')

parser.add_argument('-i1', nargs = '?', required = True, type = str, help = 'Input File 1(.wav)[ORIGINAL]')
parser.add_argument('-i2', nargs = '?', required = True, type = str, help = 'Input File 2(.wav)[SYNTHESIZED]')
parser.add_argument('-o', nargs = '?', type = str, help = 'Output Image File (Optional)')
args = parser.parse_args()

[fs1, sig1] = util.WavRead(args.i1)
[fs2, sig2] = util.WavRead(args.i2)

pad_to1 = highestPowerof2(len(sig1))
pad_to2 = highestPowerof2(len(sig2))

pad_to = min(pad_to1,pad_to2)

if fs1 != fs2:
    print('Unable to find MSE. (Sampling Freqs are different)')
    sys.exit(0)
    
sig1 = sig1/max(sig1)
spectrum1, freqs1, line1 = plot.magnitude_spectrum(sig1, Fs = fs1, scale = 'dB', pad_to = pad_to)
spectrum_db1 = 20*np.log10(spectrum1)



sig2 = sig2/max(sig2)
spectrum2, freqs2, line2 = plot.magnitude_spectrum(sig2, Fs = fs2, scale = 'dB', pad_to = pad_to)
spectrum_db2 = 20*np.log10(spectrum2)

plot.subplot(211)
y_max1 = max(spectrum_db1)+5
y_min1 = max(min(spectrum_db1)-5,-100)
plot.ylim([y_min1,y_max1])
plot.title(args.i1.split('/')[-1] + ' Spectrum_1')

#Fill Plot Like Audacity
plot.fill_between(freqs1,spectrum_db1,-110)
plot.grid()

plot.subplot(212)
y_max2 = max(spectrum_db2)+5
y_min2 = max(min(spectrum_db2)-5,-100)
plot.ylim([y_min2,y_max2])
plot.title(args.i2.split('/')[-1] + ' Spectrum_2')

#Fill Plot Like Audacity
plot.fill_between(freqs2,spectrum_db2,-110)
plot.grid()

plot.tight_layout()

#Calculate RMSE
spectrum_diff = math.sqrt(mean_squared_error(spectrum1, spectrum2))
print('RMSE = {}'.format(spectrum_diff))


plot.show()


