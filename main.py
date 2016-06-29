#!/usr/bin/env python
from __future__ import print_function
import os
import sys
import argparse
import collections


def create_parser():
    parser = argparse.ArgumentParser(description="Generate a package config file")
    parser.add_argument("-i", "--interactive", action="store_true", help="Use this flag to be prompted for package information (name, version, description)")

    parser.add_argument("-n", "--pkg_name", default="", type=str, help="The name of the package")
    parser.add_argument("-v", "--pkg_version", default="", type=str, help="The version number of the package")
    parser.add_argument("-p", "--pkg_prefix", default="", type=str, help="The prefix to be used in the package config file")
    parser.add_argument("-d", "--pkg_description", default="", type=str, help="The description for the package")
    parser.add_argument("lib_dir", type=str, help="The directory containing the library files. This is normally the 'lib' folder for your specific package.")

    parser.add_argument("-o", "--output_file", default="", type=str, help="The path to write your package config file to")

    return parser

def generate_package_file(args):

    # Python 2 uses a different version of input (compared to Python 3)
    # Let's make it so that 'input' works on both python3 and python2
    try:
        input = raw_input
    except NameError:
        import builtins;
        input = builtins.input;
        pass

    # This block let's us take input from the user and still 
    # pipe the results to an output file
    # i.e. 'python main.py -i . > example.pc' will show the prompt on 
    # screen, and write the output to 'example.pc'
    old_input = input
    def input(*args):
        old_stdout = sys.stdout
        try:
            sys.stdout = sys.stderr
            return old_input(*args)
        finally:
            sys.stdout = old_stdout

    # Helper function to generate linker commands
    # Converts library file names to linker equivalents
    # e.g. 'libboost_graph.dylib' --> '-lboost_graph'
    def generate_libs_string(lib_dir):
        """Given a lib directory, generate a string containing linker commands"""
        lib_string = ""
        libs_set = set()
        file_extensions = [".dylib", ".so", ".a"]
        file_suffix = "lib"


        # Look at all the files in the library directory
        for root, dirs, filenames in os.walk(lib_dir):
            for fname in filenames:
                extension = os.path.splitext(fname)[1]
                #  and
                if extension in file_extensions:
                    curr_linker_command = fname.replace(extension, "") 

                    if fname.startswith(file_suffix):
                        curr_linker_command = curr_linker_command.replace(file_suffix, "-l")
                    else:
                        curr_linker_command = "-l" + curr_linker_command 

                    libs_set.add(curr_linker_command)


        for libname in libs_set:
            lib_string += " " + libname

        print(libs_set)        
        print(len(libs_set))
        return lib_string

    # Create a dictionary to store the package info (name, description, libs, etc.)
    pkg_object = collections.OrderedDict() 
    pkg_object['#'] = " Package Information for pkg-config"

    # Use input from user or command line options
    if args.interactive:
        print('To skip any of these prompts, simply press enter', file=sys.stderr)

    prefix = (args.pkg_prefix == "" and args.interactive) and input('Prefix (e.g. /usr/local/Cellar/boost/1.60.0_2): ')  or args.pkg_prefix
    pkg_name = (args.pkg_name == "" and args.interactive) and input('Package name (e.g. Boost): ') or args.pkg_name
    description = (args.pkg_description == "" and args.interactive) and input("Package description: " ) or args.pkg_description
    version = (args.pkg_version == "" and args.interactive) and input('Package Version (e.g. 1.60.0): ')  or args.pkg_version

    pkg_object['prefix='] = prefix 
    pkg_object['exec_prefix='] = "${prefix}"
    pkg_object['libdir='] ="${exec_prefix}/lib"
    pkg_object['includedir_old='] = "${prefix}/include/" + pkg_name.lower() 
    pkg_object['includedir_new='] = "${prefix}/include"
    pkg_object['Name: '] = pkg_name 
    pkg_object['Description: '] = description 
    pkg_object['Version: '] = version 
    pkg_object['Libs: '] = '-L${exec_prefix}/lib ' + generate_libs_string(args.lib_dir)
    pkg_object['Cflags: '] = "-I${includedir_old} -I${includedir_new}" 

    print('', file=sys.stderr)

    # Print to stdout or to an output file (extension has to be .pc)
    f = None
    if args.output_file is not "":
        path = args.output_file
        while not path.endswith('.pc'):
            print('The filename must contain the ".pc" extension. Please change your output file name accordingly')
            path = input('File name (must end with .pc): ')
        f = open(path, 'w') 
    else:
        f = sys.stdout
    
    for key, value in pkg_object.items():
        if key == 'prefix=' or key == 'Name: ':
            print('', file=f)
        print(key + value, file=f)

def main():
    args = create_parser().parse_args()
    generate_package_file(args)

if __name__ == "__main__":
    main()
