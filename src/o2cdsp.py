#!/bin/python3
#
# Converts an Oratory1990 parametric EQ settings file to a CamillaDSP configuration file
# @bitkeeper 2021
#

import re
from base import Config2CdspConfigBase


class Oratory1990Importer (Config2CdspConfigBase):

    FILTER_CONV = {'LOW_SHELF': 'Lowshelf', 'PEAK': 'Peaking', 'HIGH_SHELF': 'Highshelf'}

    re_gain = re.compile('([-+]?\d*\,?\d*)[ ]dB')
    re_freq = re.compile('([-+]?\d*\,?\d*)[ ]Hz')
    re_float = re.compile('^[-+]?\d*\,?\d*$')

    def __init__(self):
        super().__init__()
        self.description = 'o2cdsp converts Oraratory1990 parametric EQ settings to a CamillaDSP configuration file.'

    def convert(self, file):
        gain = 0
        filters = []

        for line in file:
            if 'Band ' in line:
                ft_type = Oratory1990Importer.FILTER_CONV[file.readline().strip()]
                # ft_type = 'Peak'
                ft_freq = Oratory1990Importer.re_freq.match(file.readline()).group(1)
                ft_gain = Oratory1990Importer.re_gain.match(file.readline()).group(1).replace(',', '.')
                ft_q = Oratory1990Importer.re_float.match(file.readline()).group(0).replace(',', '.')
                ft_bw = Oratory1990Importer.re_float.match(file.readline()).group(0).replace(',', '.')

                if 'shelf' in ft_type:
                    filter=dict( type= ft_type, freq=int(ft_freq) , slope=float(1), gain=float(ft_gain))
                else:
                    filter=dict( type= ft_type, freq=int(ft_freq) , q=float(ft_q), gain=float(ft_gain))

                filters.append(filter)
                print(filter)
            elif 'Preamp gain' in line:
                gain = float(Oratory1990Importer.re_gain.match(file.readline()).group(1).replace(',', '.'))


        return gain, filters

if __name__ == "__main__":
    importer = Oratory1990Importer()
    importer.main()
