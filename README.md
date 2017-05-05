# Package Config file generator

## Overview

This is a simple python (2 or 3) script for generating package config (`pkg-config` or `.pc`) files.  Feel free to adapt it to your needs/fork it. 

What does it do?

- Interactive prompt for package info (name, version, description)
- Command line mode for those who don't like interactive
- Automatic linker command generation 

Provide it a directory with libraries (.so, .dylib, .etc) and it will generate linker commands. Try it out in the test directory to see it how it works.


## Example use

Use the interactive mode for a text prompt. There are dummy lib files in the `test_libs` directory (not real libraries, just for demonstration). 

	python main.py -i test_libs 

Provide info directly via command line. Here we provide the name, version and prefix of the package (Boost in this case). The `prefix` or `-p` represents where the main package is installed on your computer. Lastly, we write the output to a package config file (**boost.pc**) in the current directory.

	python main.py -n Boost -v 1.60.0 -p /usr/local/Cellar/boost/1.60.0_2 -o boost.pc

We can also redirect the output to a file.

	python main.py -n Boost -p /usr/local/Cellar/boost/1.60.0_2 -v 1.60.0 /usr/local/Cellar/boost/1.60.0_2 -d "Boost is awesome" > boost.pc

The paths used in these examples exist on my machine. You'll have to determine where these libraries exist on your own machine.

Once you have a .pc file, you should place it in the pkg-config path. One standard path is this directory. Check it to see if there are other .pc files there.  

	/usr/local/lib/pkgconfig/

## Usage

	usage: python main.py [-h] [-i] [-n PKG_NAME] [-v PKG_VERSION] [-p PKG_PREFIX]
		       [-d PKG_DESCRIPTION] [-o OUTPUT_FILE]
		       lib_dir

	Generate a package config file automatically-ish

	positional arguments:
	  lib_dir               The directory containing the library files. This is
				normally the 'lib' folder for your specific package.

	optional arguments:
	  -h, --help            show this help message and exit
	  -i, --interactive     Use this flag to be prompted for package information
				(name, version, description)
	  -n PKG_NAME, --pkg_name PKG_NAME
				The name of the package
	  -v PKG_VERSION, --pkg_version PKG_VERSION
				The version number of the package
	  -p PKG_PREFIX, --pkg_prefix PKG_PREFIX
				The prefix to be used in the package config file
	  -d PKG_DESCRIPTION, --pkg_description PKG_DESCRIPTION
				The description for the package
	  -o OUTPUT_FILE, --output_file OUTPUT_FILE
				The path to write your package config file to 
