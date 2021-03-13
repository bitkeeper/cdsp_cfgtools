#!/bin/python3
#
# Converts ASH-IR APO configuration file to CamillaDSP configuration file
# @bitkeeper 2021
#
#
#

import re
from base import Config2CdspConfigBase, DEVICES, STEREO_MIXER
from yaml import load, FullLoader
import os

#TODO: auto detect format of the wave file
#TODO: detect clipping level for automatic master gain

class AshIrImporter (Config2CdspConfigBase):

    FORMATS = ['TEXT',
           'FLOAT64LE',
           'FLOATLE',
           'S32LE',
           'S24LE3',
           'S24LE',
           'S16LE']

    def __init__(self):
        super().__init__()
        self.description = 'ash2cdsp creates configuration for use of ASH IR files.'
        self.convs = []
        parser = self.init_arg_parser()
        parser.add_argument('--format', dest = 'format',
                   choices = AshIrImporter.FORMATS, #default = 'other',
                   help = 'Format of the convolution files')
        parser.add_argument('--prepwave', dest = 'prep_wave', action='store_const', const = sum,
                   help = 'Prep the wav files for camilladsp by split the channeld.')
        parser.add_argument('--soxpath', dest = 'sox_path', default='sox',
                   help = 'Sox to sox exucutable (default sox)')
        parser.add_argument('--coeff-path', dest = 'coeff_path', default = None,
                   help = 'Change convolution location to this path.')
        parser.add_argument('--hpcf', dest = 'hpcf_file', default = None,
                   help = 'Headphone compensation filter file to use. If not provided only a spatial simulation config is generated')

    def get_conv_files(self, file):
        convs = []
        for line in file:
            pos = line.find('Convolution: ')
            if pos != -1:
                # conv_file = line[pos + len('Convolution: '):].strip().split('\\')[-1]
                conv_file = line[pos + len('Convolution: '):].strip()
                convs.append(conv_file)
        return convs

    def convert(self, file):
        gain = 0
        filters = []

        self.convs = self.get_conv_files(file)
        return gain, filters

    def generate(self):
        gain = self.gain
        args = self.args
        base, ext = os.path.splitext((os.path.basename(self.convs[0])) )

        ir_angle = abs(int(base[-3:]))
        ir_name = '../coeffs/'+base[:-3]
        ir_format = args.format

        # abs pathof conv relative to input config
        ir_file_input_base = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(self.inputfile)), os.path.dirname(self.convs[0]), base[:-3]) )
        wave_file_input = '{name}{{}}{angle}{ext}'.format(name=ir_file_input_base, angle=ir_angle, ext=ext)

        if args.coeff_path:
          ir_file_input_base = os.path.join(args.coeff_path, os.path.basename(ir_file_input_base) )
        ir_file_input_base = ir_file_input_base.replace('\\', '/')

        wave_file_output = '{name}{{}}{angle}_{{}}_{format}{ext}'.format(name=ir_file_input_base, angle=ir_angle, ext='.raw', format='$samplerate$Hz_32b')

        wave_files_out = [wave_file_output.format('-','L'),
                          wave_file_output.format('-','R'),
                          wave_file_output.format('','L'),
                          wave_file_output.format('','R')]

        if args.prep_wave:
          self.prep_wave(wave_file_input.format('-'), [wave_files_out[0], wave_files_out[1]])
          self.prep_wave(wave_file_input.format(''), [wave_files_out[2], wave_files_out[3]])

        if args.hpcf_file:
          template_file =  "__spatial_hpcf__ .yml"
          wave_file_output = os.path.join( os.path.dirname(ir_file_input_base), os.path.basename(args.hpcf_file)[:-4]+'_$samplerate$Hz_32b.raw')
          print(wave_file_output)
          wave_file_output = wave_file_output.replace('\\', '/')
          if args.prep_wave:
            self.prep_wave(args.hpcf_file, [wave_file_output])
        else:
          template_file =  "__spatial__.yml"

        template_file = os.path.abspath( os.path.join( os.path.dirname(os.path.abspath(__file__) ), '..', 'data', 'ash_ir_dataset', template_file ) )

        with open( template_file,  'r') as template_config_file:
          template_config_string = template_config_file.read()
          if args.hpcf_file:
            config_string = template_config_string.format(IR_FORMAT = ir_format,
                              IR_HPCF = wave_file_output,
                              IR_L_INPUT_L_EAR = wave_files_out[0],
                              IR_L_INPUT_R_EAR = wave_files_out[1],
                              IR_R_INPUT_L_EAR = wave_files_out[2],
                              IR_R_INPUT_R_EAR = wave_files_out[3])
          else:
            config_string = template_config_string.format(IR_FORMAT = ir_format,
                              IR_L_INPUT_L_EAR = wave_files_out[0],
                              IR_L_INPUT_R_EAR = wave_files_out[1],
                              IR_R_INPUT_L_EAR = wave_files_out[2],
                              IR_R_INPUT_R_EAR = wave_files_out[3])


          config = load(config_string, Loader=FullLoader)
          config['filters']['mastergain']['parameters'] ['gain'] = float(gain)
        self.config = config

    def prep_wave(self, filename, outputs):
        for idx,output in enumerate(outputs):
           output= output.replace('$samplerate$', '44100')


           output = os.path.join( os.path.dirname(self.args.output), output)
           output = os.path.abspath(output)

           if os.path.isfile(output) == False:
            if len(outputs) == 2:
                cmd ='{} {} -b 32 {} remix {}'.format(self.args.sox_path, filename, output, idx+1)
            else:
                cmd ='{} {} -b 32 {} '.format(self.args.sox_path, filename, output)
            os.system(cmd)

if __name__ == "__main__":
    importer = AshIrImporter()
    importer.main()
