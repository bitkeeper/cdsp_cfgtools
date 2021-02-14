#!/bin/python3
#
# Converts an AutoEq Parametric EQ setting file to a CamillaDSP configuration file
#
#


# PEQ:
# https://raw.githubusercontent.com/jaakkopasanen/AutoEq/master/results/oratory1990/harman_over-ear_2018/Sennheiser%20HD%20800%20S/Sennheiser%20HD%20800%20S%20ParametricEQ.txt
# CONV:
# https://raw.githubusercontent.com/jaakkopasanen/AutoEq/master/results/oratory1990/harman_over-ear_2018/Sennheiser%20HD%20800%20S/Sennheiser%20HD%20800%20S%20minimum%20phase%2044100Hz.wav
#
import re
from yaml import load, dump

re_gain = re.compile('([-+]?\d*\.?\d*)[ ]dB')
re_setting = re.compile('ON PK Fc (\d*) Hz Gain ([-+]?\d*\.?\d*) dB Q (\d*\.?\d*)$')


def autoeq_extract_peq(file):
    gain = 0
    filters = []
    for line in file:
        label, settings = line.strip().split(':')
        if label == 'Preamp':
            m = re_gain.search(settings.strip())
            if m:
                gain = float(m.group(1))
        elif 'Filter' in label:
            m = re_setting.search(settings.strip())
            if m:
                filter=dict( type= 'Peaking', freq=int(m.group(1)) , q=float(m.group(3)), gain=float(m.group(2)))
                filters.append(filter)
    return gain, filters

def gen_cdsp_peq_config(gain, filters):
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


    return config

def oraryty_extract(file):
    config = {}
    return config

def handle_aeq(autoeq_input_peq):
    with open(autoeq_input_peq, 'r') as file:
        gain, filters = autoeq_extract_peq(file)


def handle_or(oraryty_input):
    with open(oraryty_input, 'r') as file:
        gain, filters = oraryty_extract(file)


def gen_cdsp_config(gain, filters):
    config = gen_cdsp_peq_config(gain, filters)
    cdsp_config = 'config.yml'
    with open(cdsp_config, 'w') as file:
        dump(config, file, sort_keys=False)

# filename = 'autopeq.txt'
# gain, filters = handle_aeq(filename)

filename = 'oratory1990_hd800s.txt'
gain, filters = handle_aeq(filename)
gen_cdsp_config(gain, fitlers)

