import os
import platform
import shutil
import re

CWD = os.getcwd()
BUILD_PATH = os.path.join(CWD, "build")
LIB_PATH = os.path.join(CWD, "ext")


def main():
    setup_extension()
    move_extension()


def setup_extension():
    if platform.system().lower() == 'windows':
        os.system('python scripts/build_extension.py build')
    else:
        os.system('python3 scripts/build_extension.py build')


def move_extension():
    build_dirs = os.listdir(BUILD_PATH)

    try:
    	os.makedirs(LIB_PATH)
    except FileExistsError:
    	pass

    for dir in build_dirs:
        if re.search("^lib.*", dir):
            files = os.listdir(BUILD_PATH + "/" + dir)
            for file_name in files:
                src_path = os.path.join(BUILD_PATH, dir, file_name)
                dst_path = os.path.join(LIB_PATH, file_name)
                shutil.move(src_path, dst_path)

    shutil.rmtree(BUILD_PATH)


if __name__ == "__main__":
    main()
