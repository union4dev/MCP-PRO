import init
import remapper


def main():
    runtime_dir = init.get_runtime_dir()
    root_dir = init.resolve_runtime_dir(runtime_dir)
    java_path = init.check_java_version()
    version = init.get_version_from_cfg(root_dir)
    remapper.remap(version, root_dir, java_path)


if __name__ == '__main__':
    main()
