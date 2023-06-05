import os
import pathlib
import shutil
import subprocess
import sys
import time


def remap(version, root_dir, java_path):
    print('>> Backend minecraft file to temp folder')
    t = time.time()
    path = pathlib.Path(f'{os.path.expanduser("~")}/AppData/Roaming/.minecraft/versions/{version}/{version}.jar')
    if path.exists() and path.is_file():
        shutil.copy(path, f'{root_dir}/temp/minecraft_ori.jar')
    else:
        print('Failed to found client file...')
        sys.exit(1)
    print('>> Get mapping file')
    mapping = pathlib.Path(f'{root_dir}/conf/mappings.tsrg')
    special_source = pathlib.Path(f'{root_dir}/runtime/bin/specialsource.jar')
    backend = pathlib.Path(f'{root_dir}/temp/minecraft_ori.jar')
    if backend.exists() and mapping.exists() and special_source.exists() and backend.is_file() \
            and mapping.is_file() and special_source.is_file():
        backend = backend.resolve()
        mapping = mapping.resolve()
        special_source = special_source.resolve()
        print(java_path)
        subprocess.run([
            f'{java_path}/Java.exe',
            '-jar', special_source.__str__(),
            '--in-jar', backend.__str__(),
            '--out-jar', f'{root_dir}/temp/minecraft_remapped.jar',
            '--srg-in', mapping.__str__(),
            '-kill-lvt'
        ], check=True, stdout=subprocess.STDOUT, capture_output=False)
        print('>> Remapped')
        delta_time = time.time() - t
        print('[REMAP] Done in %.1fs' % delta_time)
    else:
        print('[REMAP] Missing files...')
        sys.exit(1)