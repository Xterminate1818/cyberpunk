from subprocess import call
from glob import glob
from configparser import ConfigParser
import sys
import os
from collections import defaultdict


def find_files(path: str, pattern: str, recursive: bool=False, extension: bool=False) -> list:
    files = []
    for fname in glob(path + pattern, recursive=recursive):
        if extension:
            files.append(fname)
        else:
            files.append(os.path.splitext(fname)[0])
    return files

def log(msg: str) -> None:
    print("[PYMAKE] " + msg + "\u001b[0m")


def shell(cmd: str, silent=False) -> int:
    if not silent:
        log(cmd)
    return call(cmd, shell=True)

def fail_if(exit_code, message: str) -> None:
    if (type(exit_code) == int and exit_code != 0) or (type(exit_code) == bool and exit_code == True):
        log("\u001b[31m" + message)
        sys.exit()


if __name__ == "__main__":
    default_config: dict = {
        "exe_name" : "Program",
        "exe_dir" : "./bin/",
        "compiler" : "g++",
        "compiler_flags" : "-g -Wall -Wextra",
        "linker_flags" : "",
        "source_path" : "./src/",
        "bin_path" : "./bin/"
    }
    bld: defaultdict = defaultdict(lambda: "")
    bld = default_config

    # If build type is not default
    if len(sys.argv) > 1:
        cfg = ConfigParser()
        found = cfg.read("build.ini")
        fail_if(len(found) == 0, "Build type provided but no 'build.ini' file found!")
        argument = sys.argv[1]
        if argument.upper() == "DEFAULT":
            argument = "DEFAULT"
        fail_if(argument != "DEFAULT" and not cfg.has_section(argument), "Cannot find build type in config file!")
        bld = default_config | (dict(cfg[argument]))
        log(f"Using config profile: %s" % argument)
    else:
        log("Using config profile: DEFAULT")

    # Check for valid config
    fail_if(not os.path.exists(bld["bin_path"]), "Provided 'bin_path' does not exist!")
    fail_if(not os.path.exists(bld["source_path"]), "Provided 'src_path' does not exist!")
    fail_if(bld["exe_name"] == "", "Provided 'exe_name' is an empty string!")
    fail_if(
            shell(f"which %s" % bld["compiler"], silent=True), 
            "Provided 'compiler' does not exist!"
            )
    
    # Cleaning step - Don't care if this errors
    log("Cleaning up...")
    shell(f"rm %s*.o" % (bld["bin_path"]))

    # Compilation step
    exit_code = 0
    log("Compiling...")
    src_files = find_files(bld["source_path"], "*.cpp", recursive=True)
    for f in src_files:
        exit_code = shell(f"%s -c %s.cpp %s" % (bld["compiler"], f, bld["compiler_flags"]))
        fail_if(exit_code, "Compilation failed!")

    # Moving object files to bin directory
    o_files = find_files("./", "*.o")
    for f in o_files:
        exit_code = shell("mv %s.o %s%s.o" % (f, bld["bin_path"], f))
        fail_if(exit_code, "Failed to move object files!")

    # Linking step
    log("Linking...")
    o_files = find_files(bld["bin_path"], "*.o", recursive=False, extension=True)
    exit_code = shell(f"%s -o %s%s %s %s" %
            (bld["compiler"], bld["exe_dir"], bld["exe_name"], 
            " ".join(o_files), bld["linker_flags"]))
    fail_if(exit_code, "Linking failed!")
    log("\u001b[32mSuccess!")

