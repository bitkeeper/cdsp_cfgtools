
import glob
import os
from ash2cdsp import AshIrImporter

if __name__ == "__main__":
    ash_path = 'D:\\work\\ASH-IR-Dataset'

    glob_path = os.path.join(ash_path, 'E-APO_Configs', 'BRIR_Convolution', '2.0_Stereo', '*.txt')
    print(glob_path)
    files = glob.glob(glob_path)

    for ashconfig in files:
        # // print(ashconfig)
        print(os.path.splitext(os.path.basename(ashconfig))[0])
        with open(ashconfig, 'r') as file:
            # line = file.read()
            # print(line)
            for line in file:
                # print(line)
                pos = line.find('Convolution: ')
                # if 'Convolution: ' in line:
                # if pos != -1:
                #     conv_file = line[pos + len('Convolution: '):].strip().split('\\')[-1]
                #     print(conv_file)
                #     print(os.path.splitext(conv_file)[0])
            cdsp_cfgfile = os.path.join('..', 'out', 'ash_ir_dataset', 'configs', os.path.splitext(os.path.basename(ashconfig))[0]+'.yml')
            # if os.path.isfile(cdsp_cfgfile):
            #     print('OEPS not found')
            #     exit(1)
            # ashconfig = ashconfig.replace('\\', '/')
            # print(cdsp_cfgfile)
            # print(ashconfig)
            sox_path = r"D:\Programs\sox-14.4.2\sox.exe"
            hpcf_file = r"D:\work\ASH-IR-Dataset\HpCFs\Sennheiser\HpCF_Sennheiser_HD800S_A.wav"
            imp = AshIrImporter()
            # imp.import_file(ashconfig, cdsp_cfgfile)
            cmd ='--output {} --coeff-path ../coeffs --format S32LE --gain -9 --prepwave --hpcf {} --soxpath {} {}'.format(cdsp_cfgfile, hpcf_file, sox_path, ashconfig)

            cmd = cmd.split(' ')
            # print(cmd)
            imp.main(cmd)



