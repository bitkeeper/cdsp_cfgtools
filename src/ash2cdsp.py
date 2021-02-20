#!/bin/python3
#
# Converts ASH-IR APO configuration file to CamillaDSP configuration file
# @bitkeeper 2021
#

import re
from base import Config2CdspConfigBase, DEVICES, STEREO_MIXER
from yaml import load, FullLoader
import os

#TODO: support more then a fixed WAVE file for 16_SE
#TODO: auto detect format of the wave file
#TODO: detect clipping level for automatic master gain

ASH_IR_TEMPLATE ='''
devices:
  adjust_period: 10
  capture:
    channels: 2
    extra_samples: 0
    filename: /dev/stdin
    format: S32LE
    read_bytes: 0
    skip_bytes: 0
    type: File
  capture_samplerate: 0
  chunksize: 1024
  enable_rate_adjust: false
  enable_resampling: false
  playback:
    channels: 2
    device: hw:0,0
    format: S32LE
    type: Alsa
  queuelimit: 1
  resampler_type: BalancedAsync
  samplerate: 44100
  silence_threshold: 0
  silence_timeout: 0
  target_level: 0
filters:
  mastergain:
    type: Gain
    parameters:
      gain: 3
      inverted: false
  ir_l_input_l_ear:
    type: Conv
    parameters:
      type: File
      filename: {IR_L_INPUT_L_EAR}
      format: {IR_FORMAT}
  ir_l_input_r_ear:
    type: Conv
    parameters:
      type: File
      filename: {IR_L_INPUT_R_EAR}
      format: {IR_FORMAT}

  ir_r_input_l_ear:
    type: Conv
    parameters:
      type: File
      filename: {IR_R_INPUT_L_EAR}
      format: {IR_FORMAT}
  ir_r_input_r_ear:
    type: Conv
    parameters:
      type: File
      filename: {IR_R_INPUT_R_EAR}
      format: {IR_FORMAT}
mixers:
  2to4:
    channels:
      in: 2
      out: 4
    mapping:
    - dest: 0
      sources:
      - channel: 0
        gain: 0
        inverted: false
    - dest: 1
      sources:
      - channel: 0
        gain: 0
        inverted: false
    - dest: 2
      sources:
      - channel: 1
        gain: 0
        inverted: false
    - dest: 3
      sources:
      - channel: 1
        gain: 0
        inverted: false
  4to2:
    channels:
      in: 4
      out: 2
    mapping:
    - dest: 0
      sources:
      - channel: 0
        gain: 0
        inverted: false
      - channel: 2
        gain: 0
        inverted: false
    - dest: 1
      sources:
      - channel: 1
        gain: 0
        inverted: false
      - channel: 3
        gain: 0
        inverted: false
pipeline:
- type: Filter
  channel: 0
  names:
  - mastergain
- type: Filter
  channel: 1
  names:
  - mastergain
- type: Mixer
  name: 2to4
- type: Filter
  channel: 0
  names:
  - ir_l_input_l_ear
- type: Filter
  channel: 1
  names:
  - ir_l_input_r_ear
- type: Filter
  channel: 2
  names:
  - ir_r_input_l_ear
- type: Filter
  channel: 3
  names:
  - ir_r_input_r_ear
- type: Mixer
  name: 4to2
'''


class AshIrImporter (Config2CdspConfigBase):

    def __init__(self):
        super().__init__()
        self.description = 'ash2cdsp creates configuration for use of ASH IR files.'
        self.convs = []

    def get_conv_files(self, file):
        convs = []
        for line in file:
            pos = line.find('Convolution: ')
            if pos != -1:
                conv_file = line[pos + len('Convolution: '):].strip().split('\\')[-1]
                convs.append(conv_file)
        return convs

    def convert(self, file):
        gain = 0
        filters = []

        self.convs = self.get_conv_files(file)

        return gain, filters


    def generate(self):
        gain = self.gain
        # config = {'devices': DEVICES }

        # conv_file = line[pos + len('Convolution: '):].strip().split('\\')[-1]
        base, ext = os.path.splitext(self.convs[0])

        ir_angle = abs(int(base[-3:]))
        ir_name = '../coeffs/'+base[:-3]
        ir_format = 'S16LE'

        config_string = ASH_IR_TEMPLATE.format(IR_FORMAT = ir_format,
                            IR_L_INPUT_L_EAR = '{}-{}_L{}'.format(ir_name, ir_angle, ext),
                            IR_L_INPUT_R_EAR = '{}-{}_R{}'.format(ir_name, ir_angle, ext),
                            IR_R_INPUT_L_EAR = '{}{}_L{}'.format(ir_name, ir_angle, ext),
                            IR_R_INPUT_R_EAR = '{}{}_R{}'.format(ir_name, ir_angle, ext),
        )

        config = load(config_string, Loader=FullLoader)
        config['filters']['mastergain']['parameters'] ['gain'] = float(gain)
        self.config = config


if __name__ == "__main__":
    importer = AshIrImporter()
    importer.main()
