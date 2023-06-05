import pathlib
import subprocess
import sys
import time


def apply_cfr(root_dir, java_path):
    print('>> Decompiling by CFR (Please wait, this may taking a long time)')
    t = time.time()
    remapped = pathlib.Path(f'{root_dir}/temp/minecraft_remapped.jar')
    cfr = pathlib.Path(f'{root_dir}/runtime/bin/cfr-0.152.jar')
    if remapped.exists() and remapped.is_file() and cfr.exists() and cfr.is_file():
        remapped = remapped.resolve()
        cfr = cfr.resolve()
        print('>> Start decompile')
        subprocess.run([
            f'{java_path}/Java.exe',
            '-jar', cfr.__str__(),
            remapped.__str__(),
            '--outputdir', f'{root_dir}/temp/cfr_decompiled'
        ], check=True, capture_output=False)
        print('>> CFR Decompiled')
        delta_time = time.time() - t
        print('[DECOMP/CFR] Done in %.1fs' % delta_time)
    else:
        print('[DECOMP/CFR] Missing files...')
        sys.exit(1)


def get_cfr_errors(root_dir):
    print('>> Try to get cfr decompile failed messages')
    summary = pathlib.Path(f'{root_dir}/temp/cfr_decompiled/summary.txt')
    if summary.exists() and summary.is_file():
        summary = summary.resolve()
        with open(summary.__str__(), encoding='utf-8', mode='r') as reading_file:
            lines = reading_file.readlines()
            errors = []
            counter = 0
            for line in lines:
                if (line.__contains__('Unable to fully structure code')
                    or line.__contains__('Exception : org.benf.cfr.reader')) \
                        and counter >= 4:
                    error_code = line.replace('\n', '').replace(' ', '')
                    error_method = lines[counter - 1].replace('\n', '').replace(' ', '')
                    error_class = lines[counter - 4].replace('\n', '').replace(' ', '')
                    errors.append(ErrorData(error_code, error_method, error_class))

                counter = counter + 1
            return errors
    else:
        print('[DECOMP/FIXER] Missing files...')
        sys.exit(1)


class ErrorData(object):
    def __init__(self, error_code, error_method, error_class):
        self.error_code = error_code
        self.error_method = error_method
        self.error_class = error_class
