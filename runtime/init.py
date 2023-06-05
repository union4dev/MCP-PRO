import os
import pathlib
import subprocess
import sys


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