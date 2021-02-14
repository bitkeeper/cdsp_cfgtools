#!/bin/python3
#
# Converts an AutoEq 10 band parametric EQ settings file to a CamillaDSP configuration file
# @bitkeeper 2021
#

import re
from base import Config2CdspConfigBase


class AutoEqImporter (Config2CdspConfigBase):

    re_gain = re.compile('([-+]?\d*\.?\d*)[ ]dB')
    re_setting = re.compile('ON PK Fc (\d*) Hz Gain ([-+]?\d*\.?\d*) dB Q (\d*\.?\d*)$')

    def __init__(self):
        super().__init__()
        self.description = 'ae2cdsp converts AutoEQ parametric EQ settings to a CamillaDSP configuration file.'

    def convert(self, file):
        gain = 0
        filters = []
        first_line = True
        for line in file:
            label, settings = line.strip().split(':')
            if label == 'Preamp':
                m = AutoEqImporter.re_gain.search(settings.strip())
                if m:
                    gain = float(m.group(1))
                    first_line = False
            elif first_line:
                raise "Error: This file isn't a Auto Eq paramatric equalizer settings file"
            elif 'Filter' in label:
                m = AutoEqImporter.re_setting.search(settings.strip())
                if m:
                    filter=dict( type= 'Peaking', freq=int(m.group(1)) , q=float(m.group(3)), gain=float(m.group(2)))
                    filters.append(filter)
        return gain, filters

if __name__ == "__main__":
    importer = AutoEqImporter()
    importer.main()
