from subprocess import call
from glob import glob
from configparser import ConfigParser
import sys
import os
from collections import defaultdict


def find_files(_path: str, _pattern: str, _rec: bool = False, _ext: bool = False) -> list:
    '''
    Return list of file path strings inside of folder _path matching _pattern.
        _rec: recursive True/False (default False)
        _ext: include extension True/False (default False)
    '''
    files = []
    for fname in glob(_path + _pattern, recursive=_rec):
        if _ext:
            files.append(fname)
        else:
            files.append(os.path.splitext(fname)[0])
    return files


def log(_msg: str) -> None:
    '''
    Print message to output with [PYMAKE] prefix, end with ANSI reset code.
    '''
    print("[PYMAKE] " + _msg + "\u001b[0m")


def shell(_cmd: str, _silent: bool = False) -> int:
    '''
    Run _cmd as a shell command, disable echo with _silent=True
    '''
    if not _silent:
        log(_cmd)
    return call(_cmd, shell=True)


def fail_if(_exit, _msg: str) -> None:
    '''
    Do sys.exit() and log _msg if _exit is a non-zero int or a boolean True
    '''
    if (isinstance(_exit, int) and _exit != 0) or (isinstance(_exit, bool) and _exit == True):
        log("\u001b[31m" + _msg)
        sys.exit()


if __name__ == "__main__":
    default_config = {
        "exe_name": "Program",
        "exe_dir": "./bin/",
        "compiler": "g++",
        "compiler_flags": "-g -Wall -Wextra",
        "linker_flags": "",
        "source_path": "./src/",
        "bin_path": "./bin/"
    }
    bld: defaultdict = defaultdict(lambda: "")
    bld = default_config

    # If build type is not default
    if len(sys.argv) > 1:
        cfg = ConfigParser()
        found = cfg.read("build.ini")
        fail_if(len(found) == 0,
                "Build type provided but no 'build.ini' file found!")
        ARG = sys.argv[1]
        if ARG.upper() == "DEFAULT":
            ARG = "DEFAULT"
        fail_if(ARG != "DEFAULT" and not cfg.has_section(
            ARG), "Cannot find build type in config file!")
        bld = default_config | (dict(cfg[ARG]))
        log(f"Using config profile: {ARG}")
    else:
        log("Using config profile: DEFAULT")

    # Check for valid config
    fail_if(not os.path.exists(bld["bin_path"]),
            "Provided 'bin_path' does not exist!")
    fail_if(not os.path.exists(bld["source_path"]),
            "Provided 'src_path' does not exist!")
    fail_if(bld["exe_name"] == "", "Provided 'exe_name' is an empty string!")
    fail_if(
        shell(f"which {bld['compiler']}", _silent=True),
        "Provided 'compiler' does not exist!"
    )

    # Cleaning step - Don't care if this errors
    log("Cleaning up...")
    shell(f"rm {bld['bin_path']}*.o")

    # Compilation step
    exit_code = 0
    log("Compiling...")
    src_files = find_files(bld["source_path"], "*.cpp", _rec=True)
    for f in src_files:
        exit_code = shell(
            f"{bld['compiler']} -c {f}.cpp {bld['compiler_flags']}")
        fail_if(exit_code, "Compilation failed!")

    # Moving object files to bin directory
    O_FILES = find_files("./", "*.o")
    for f in O_FILES:
        exit_code = shell(f"mv {f}.o {bld['bin_path']}{f}.o")
        fail_if(exit_code, "Failed to move object files!")

    # Linking step
    log("Linking...")
    O_FILES = " ".join(find_files(
        bld["bin_path"], "*.o", _rec=False, _ext=True))
    exit_code = shell(
        f"{bld['compiler']} -o {bld['exe_dir']}{bld['exe_name']} {O_FILES} {bld['linker_flags']}")
    fail_if(exit_code, "Linking failed!")
    log("\u001b[32mSuccess!")
