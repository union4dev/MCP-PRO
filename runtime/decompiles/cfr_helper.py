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
