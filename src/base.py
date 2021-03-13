from yaml import dump
import argparse

DEVICES = {
  'adjust_period': 10,
  'capture': {
    'channels': 2,
    'extra_samples': 0,
    'filename': '/dev/stdin',
    'format': 'S32LE',
    'read_bytes': 0,
    'skip_bytes': 0,
    'type': 'File'
   },
  'capture_samplerate': 0,
  'chunksize': 1024,
  'enable_rate_adjust': False,
  'enable_resampling': False,
  'playback': {
    'channels': 2,
    'device': 'hw:0,0',
    'format': 'S32LE',
    'type': 'Alsa',
   },
  'queuelimit': 1,
  'resampler_type': 'BalancedAsync',
  'samplerate': 44100,
  'silence_threshold': 0,
  'silence_timeout': 0,
  'target_level': 0
}

STEREO_MIXER = {
    'channels': {
      'in': 2,
      'out': 2
      },
    'mapping': [ {
        'dest': 0,
        'sources': [ {
            'channel': 0,
            'gain': 0,
            'inverted': False
            }
        ]}, {
        'dest': 1,
        'sources': [{
            'channel': 1,
            'gain': 0,
            'inverted': False
            }
        ]
        }
    ]
}

class Config2CdspConfigBase:
    VERSION = "0.1.0"

    def __init__(self):
        super().__init__()
        self.gain = None
        self.filters = []
        self.epilog =''
        self.description =''

        self.parser = None

    def generate(self):
        gain = self.gain
        filters = self.filters
        config = {'devices': DEVICES }

        config['filters'] = {}
        config['filters']['peqgain'] = { 'type': 'Gain',
                                        'parameters': {'gain': gain, 'inverted': False }}
        for idx, filter in enumerate(filters):
            filter_config = {'type': 'Biquad'}
            filter_config['parameters'] =  filter

            config['filters'] ['band_{:02d}'.format(idx+1)] = filter_config

        config['mixers'] = {'stereo': STEREO_MIXER}

        config['pipeline'] = []
        config['pipeline'].append( {'type': 'Mixer', 'name': 'stereo'})
        config['pipeline'].append( { 'type': 'Filter', 'channel': 0, 'names': list(config['filters'].keys())} )
        config['pipeline'].append( { 'type': 'Filter', 'channel': 1, 'names': list(config['filters'].keys())} )

        self.config = config
        # return config

    def export_to_file(self, filename):
        with open(filename, 'w') as file:
            dump(self.config, file, sort_keys=False)

    def import_file(self, inputfilename, outputfilename):
        inputfilename = inputfilename.replace('\\\\', '\\')

        with open(inputfilename, 'r') as file:
            self.inputfile = inputfilename
            gain, filters = self.convert(file)
            if not(self.gain):
                self.gain = gain
            self.filters = filters

        self.generate()
        self.export_to_file(outputfilename)

    def init_arg_parser(self):
        # epilog = 'Root privileges required for import or clear.'
        parser = argparse.ArgumentParser(description = self.description, epilog = self.epilog)
        parser.add_argument('inputfile',  default = None, nargs =1,
                    help = 'Input configuration of source.')

        parser.add_argument('--version', action='version', version='%(prog)s {}'.format(Config2CdspConfigBase.VERSION))
        # group = parser.add_mutually_exclusive_group( required = True)

        parser.add_argument('--gain', default = None,
                    help = 'Use this as gain (dB) in the extension, if present in inputfile it will be overruled by this one.')

        parser.add_argument('--output', default = None,
                    help = 'Output File name of the CamillaDSP config. default the input with as extension .yml')
        self.parser = parser
        return parser

    def get_cmdline_arguments(self, arguments=None):
        if self.parser == None:
            self.init_arg_parser()
        args = self.parser.parse_args(arguments) if arguments else self.parser.parse_args()
        self.args = args
        return args

    def main(self, arguments = None):
        args = self.get_cmdline_arguments(arguments)
        if args.gain:
            self.gain = float(args.gain)

        if args.inputfile:
            self.import_file(args.inputfile[0], args.output)
