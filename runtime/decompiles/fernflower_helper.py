import pathlib
import subprocess
import sys
import time


def apply_fern_flower(root_dir, java_path):
    print('>> Decompiling by FernFlower (Please wait, this may taking a long time)')
    t = time.time()
    remapped = pathlib.Path(f'{root_dir}/temp/minecraft_remapped.jar')
    fern_flower = pathlib.Path(f'{root_dir}/runtime/bin/fernflower.jar')
    ff_decomp = pathlib.Path(f'{root_dir}/temp/ff_decompiled')
    if not ff_decomp.exists():
        ff_decomp.mkdir()
    if fern_flower.exists() and fern_flower.is_file() and remapped.exists() and remapped.is_file():
        remapped = remapped.resolve()
        fern_flower = fern_flower.resolve()

        subprocess.run([
            f'{java_path}/Java.exe',
            '-jar', fern_flower.__str__(),
            '-lit=1',
            '-log=WARNING',
            remapped.__str__(),
            f'{root_dir}/temp/ff_decompiled'
        ], check=True, capture_output=False)
        print('>> FernFlower Decompiled')
        delta_time = time.time() - t
        print('[DECOMP/FernFlower] Done in %.1fs' % delta_time)
    else:
        print('[DECOMP/FernFlower] Missing files...')
        sys.exit(1)
