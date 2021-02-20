#!/bin/python3
#
# Generate a stereo convolution based CamillaDSP configuration file
# @bitkeeper 2021
#

import re
from base import Config2CdspConfigBase, DEVICES, STEREO_MIXER


#TODO: support more then a fixed WAVE file for 16_SE
#TODO: auto detect format of the wave file
#TODO: detect clipping level for automatic master gain

class ConvImporter (Config2CdspConfigBase):

    def __init__(self):
        super().__init__()
        self.description = 'ae2cdsp converts AutoEQ parametric EQ settings to a CamillaDSP configuration file.'

    def convert(self, file):
        gain = 0
        filters = []
        return gain, filters


    def generate(self):
        gain = self.gain
        config = {'devices': DEVICES }

        ir_filename = self.inputfile
        ir_format = 'S16LE'

        config['filters'] = {}
        config['filters']['mastergain'] = { 'type': 'Gain',
                                        'parameters': {'gain': gain, 'inverted': False }}
        # config['filters']['ir_left'] = { 'type': 'Conv',
        #                                 'parameters': {'type': 'file', 'filename': ir_filename , 'format': ir_format}}
        config['filters']['ir'] = { 'type': 'Conv',
                                        'parameters': {'type': 'File', 'filename': ir_filename , 'format': ir_format}}

        config['mixers'] = {'stereo': STEREO_MIXER}

        config['pipeline'] = []
        config['pipeline'].append( {'type': 'Mixer', 'name': 'stereo'})
        config['pipeline'].append( { 'type': 'Filter', 'channel': 0, 'names': ['mastergain', 'ir']} )
        config['pipeline'].append( { 'type': 'Filter', 'channel': 1, 'names': ['mastergain', 'ir']} )
        self.config = config


if __name__ == "__main__":
    importer = ConvImporter()
    importer.main()
