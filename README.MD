# cdsp_cfgtools
A library and tools for generating [CamillaDSP](https://github.com/HEnquist/camilladsp) configuration files.

Currently supported source:
- [AutoEq](https://github.com/jaakkopasanen/AutoEq) parametric EQ settings file
- [Oratory1990 presets](https://www.reddit.com/r/oratory1990/wiki/index/list_of_presets) extracted from pdf
- Single convolution impulse response file like WAVE or text
- [ASH-IR Dataset ](https://github.com/ShanonPearce/ASH-IR-Dataset) binaural room impulse responses

## Install

_Too premature yet_

Dependencies:
* Python 3
* pyyml (installed by setup.py)

```
pip setup.py .
```

## Use with AutoEq

Go to the AutoEq Github page and browse over the results.
* The first directory to select is the origin of headphone measurement.
* Second is the type of curve corrected to.
  * AutoEQ default has only generated for the Harman curve, but if you clone the project local checkout the you can generate for a lot more [curves](https://github.com/jaakkopasanen/AutoEq/tree/master/compensation).
* Next select your headphone directory
* Select `YOURMODEL ParametricEQ.txt`. For example Oratory1990 based measurment for the Sennheiser [HD800S](https://github.com/jaakkopasanen/AutoEq/blob/master/results/oratory1990/harman_over-ear_2018/Sennheiser%20HD%20800%20S/Sennheiser%20HD%20800%20S%20ParametricEQ.txt)
* Right click on the RAW button as choose save link as.
* Run the conversion tool:
```bash
ae2cdsp.py --output "ae_oratory1990_hd800s.yml" "Sennheiser HD 800 S ParametricEQ.txt"
```

## Use with Oratory1990 presets

The presets of [Oratory1990 presets](https://www.reddit.com/r/oratory1990/wiki/index/list_of_presets) are placed in a PDF file.
The converter does include a pdf parser. So we have to prepare a configuration file by copying to blocks of settings to a text file.
* Go the [Oratory1990 presets](https://www.reddit.com/r/oratory1990/wiki/index/list_of_presets)
* Search for the correct headphone model
* Download the PDF with preset
* Open the PDF

* Select `Preamp gain` block
* Paste in a fresh text document (notepad etc will due)
* Select the `Filter Settings` block
* Paste it after the preamp settings
* If everything went well you see something like:
```
Preamp gain:
-4,0 dB
Filter Settings
Filter Type
Frequency
Gain
Q-Factor
BW / S
Band 1
LOW_SHELF
115 Hz
4,0 dB
0,7
0,29
Band 2
PEAK
220 Hz
-4,9 dB
0,35
...
```
* Save it
* Run the conversion tooling:
```bash
o2cdsp.py --output "oratory1990_hd800s.yml" "oratory1990_hd800s.txt"
```

## Use with Convolution files

_Currently only support for 16 bit mono WAVEFILE is supported._
You need a impulse response file for the convolution.

For example the AutoEQ project also provide those:
* follow the same step as with AutoEQ parametric eq, but know select the [wanted](https://github.com/jaakkopasanen/AutoEq/tree/master/results/oratory1990/harman_over-ear_2018/Sennheiser%20HD%20800%20S) WAVE file and download it.
* Run the conversion tooling, including a gain to prevent clippig (check that afterwards with the camillagui tooling)

'''bash
conv2cdsp.py --gain -15 --output conv_ae_oratory19990_hd800s.yml "Sennheiser HD 800 S minimum phase 44100Hz.wav"
'''
When you copy this configuration file to somewhere else, don't forget to also copy the inputfile.
If the relative path between the yml file the convolution change, you will have to correct the path manual in the yml file.

## Customizing

### Using a different settings template for CamillaDSP

For generating a part of the settings a template is used. This contains among others the input and output device.

### Using a different gain

With `--gain` argument a gain can be applied or overruled if not already present.


## Use ASH-IR Dataset

'''
usage: ash2cdsp.py [-h] [--version] [--gain GAIN] [--output OUTPUT]
                   [--format {TEXT,FLOAT64LE,FLOATLE,S32LE,S24LE3,S24LE,S16LE}]
                   [--prepwave] [--soxpath SOX_PATH] [--coeff-path COEFF_PATH]
                   [--hpcf HPCF_FILE]
                   inputfile
'''

Minimal example
'''bash
ash2cdsp.py --gain -18 --output ../out/R02_Control_Room1.yml ..\data\2.0_Config_02_Control_Room_1.txt
'''

Full blown:
- Convert APO config to camilladdsp
- Include headphone correction
- Convert ir headphone wave file to raw file
- Convert both ir spatial wave files from stereo to 4 raw files

'''bash
ash2cdsp.py --gain -18 --format S32LE --prepwave --soxpath sox --coeff-path ../coeffs --hpcf "D:\work\ASH-IR-Dataset\HpCFs\Sennheiser\HpCF_Sennheiser_HD800S_A.wav" --output ../out/ash_ir_dataset/configs/R02_Control_Room1.yml D:\work\ASH-IR-Dataset\E-APO_Configs\BRIR_Convolution\2.0_Stereo\2.0_Config_02_Control_Room_1.txt
'''bash
