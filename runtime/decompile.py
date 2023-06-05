import os
import pathlib
import shutil
import subprocess
import sys
import time


def main():
    runtime_dir = get_runtime_dir()
    root_dir = resolve_runtime_dir(runtime_dir)
    java_path = check_java_version()
    version = get_version_from_cfg(root_dir)
    remap(version, root_dir, java_path)


def remap(version, root_dir, java_path):
    print('>> Backend minecraft file to temp folder')
    t = time.time()
    path = pathlib.Path(f'{os.path.expanduser("~")}/AppData/Roaming/.minecraft/versions/{version}/{version}.jar')
    if path.exists() and path.is_file():
        shutil.copy(path, '../temp/minecraft_ori.jar')
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
        subprocess.run([f'{java_path}/Java.exe',
                        '-jar', special_source.__str__(),
                        '--in-jar', backend.__str__(),
                        '--out-jar', f'{root_dir}/temp/minecraft_remapped.jar',
                        '--srg-in', mapping.__str__(),
                        '-kill-lvt'], check=True, capture_output=False)
        print('>> Remapped')
        delta_time = time.time() - t
        print('[REMAP] Done in %.1fs' % delta_time)
    else:
        print('[REMAP] Missing files...')
        sys.exit(1)


def get_version_from_cfg(root_dir):
    print('>> Loading config')
    file = 0
    try:
        file = open(f'{root_dir}/conf/version.cfg')
    except IOError as err:
        print(err)

    if file == 0:
        print('Failed to get cfg file...')
        sys.exit(1)

    line = file.readline()
    while line:
        if line.startswith('ClientVersion'):
            return line.replace('ClientVersion = ', '').replace('\n', '')
        line = file.readline()
    file.close()


def get_runtime_dir():
    return os.path.dirname(os.path.abspath(__file__))


def resolve_runtime_dir(runtime_dir):
    if str(runtime_dir).endswith('\\runtime'):
        path = pathlib.Path('../')
        if path.exists() and path.is_dir():
            return path.resolve().absolute().__str__()
        else:
            print('Runtime error.')
            sys.exit(1)
    elif str(runtime_dir).endswith('bin'):
        path = pathlib.Path('../../')
        if path.exists() and path.is_dir():
            return path.resolve().absolute().__str__()
        else:
            print('Runtime error.')
            sys.exit(1)
    else:
        path = pathlib.Path(runtime_dir)
        if path.exists() and path.is_dir():
            return runtime_dir
        else:
            print('Runtime error.')
            sys.exit(1)


def check_java_version():
    command_ptr = subprocess.getoutput('java -version')
    line = command_ptr.splitlines()
    if not line[0].split('"')[1].startswith('17'):
        print('You need install JDK-17 first or change your %JAVA_HOME% to JDK-17 root.')
        option = input('Or you can set your java path manually (y/n) >> ')
        if option == 'y' or option == 'Y':
            return input('Set your java path manually (up to "bin" folder) >> ')
        elif option == 'n' or option == 'N':
            print('Progress end.')
        else:
            print('Wrong input.')
        sys.exit(1)
    else:
        path = pathlib.Path('%JAVA_HOME%')
        return f'{path.resolve().absolute().__str__()}/bin'


if __name__ == '__main__':
    main()
