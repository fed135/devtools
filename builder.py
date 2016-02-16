#!/usr/bin/python

"""

Simple Manifest Builder

Author:
    Frederic Charette <fredericcharette@gmail.com>

Version:
    1.0.2

Repository:
    https://github.com/fed135/manifest-builder

Copyright:
    GNU Licence 2014

Description:
    Allows you to scan a folder structure and generate one global 
    manifest, or multiple ones in each folder. 

Running:
    python builder.py [target_folder] [options]

Options:
    -a    file paths will be absolute instead of relative
    -d    includes directories in the manifest
    -l    will output a local manifest in each folder instead of a global one
    -s    adds file size in the manifest (bytes)
    -v    verbose mode


"""

import json
import os
import sys

#The list of command line options
OPTIONS = {
    '-a':'absolute',
    '-d':'directories',
    '-l':'local',
    '-s':'size',
    '-v':'verbose'
}

#The list of colors for cli output
COLORS = {
    'BLUE' : '\033[94m',
    'GREEN' : '\033[92m',
    'YELLOW' : '\033[93m',
    'RED' : '\033[91m',
    'ENDC' : '\033[0m'
}

class ManifestBuilder(object):
    
    """
    Main class of the program.
    
    Crawls through the folder structure and outputs the manifest file(s)

    Args:
        settings: a Data structure containing the options passed to
            the program.
    """

    global_manifest=[]
    local_manifest=[]

    def __init__(self, settings={dir:'.'}):
        self.settings = settings
        self.start_scan(settings.dir)


    def start_scan(self, dir):

        """
        Initiates the recursive crawl through the directories.

            Args:
                dir: The directory to start the scan in
                
        """

        self.log('Scanning directory ' + dir + '...')
        self.scan_directory(dir, dir, '', self.global_manifest)
        for root, dirs, files in os.walk(dir):
            for folder in dirs:
                if self.settings.local :
                    self.local_manifest = []
                    self.scan_directory(dir, folder, root, self.local_manifest)
                    self.write_manifest(folder, root, self.local_manifest)
                else :
                    self.scan_directory(dir, folder, root, self.global_manifest)

        
        self.write_manifest(dir, root, self.global_manifest)
        self.log('Scan completed!')


    def scan_directory(self, start, dir, root, manifest):

        """
        Scans the provided directory and adds the files to the 
        appropriate manifest.

            Args:
                dir: The directory to scan
                root: The location of the root directory
                manifest: The manifest to add the files to
                
        """

        fullpath = ""
        isfile = False
        entry = {}
        trimmed_local_path = root.replace(start, '')[1:]

        for item in os.listdir(os.path.join(root, dir)):
            fullpath = os.path.join(root, dir, item)
            isfile = os.path.isfile(fullpath)
            entry = {}
            
            #Add entry path to manifest
            if self.settings.absolute :
                entry['path'] = fullpath
            else :
                if root == "" :
                    entry['path'] = item
                else :
                    entry['path'] = os.path.join(trimmed_local_path, dir, item)

            if isfile == False & self.settings.directories == False:
                continue

            #Add entry size to manifest
            if self.settings.size & isfile:
                entry['size'] = os.path.getsize(fullpath)

            manifest.append(entry)


    def log(self, msg='', color=COLORS['ENDC']):

        """
        Outputs a string in the cli, only in verbose mode

            Args:
                msg: The string to output
                color: The color to put the string into
        """

        if self.settings.verbose:
            print color+msg+COLORS['ENDC']

    def write_manifest(self, dir, root, manifest):

        """
        Writes the manifest file at the specified location

            Args:
                dir: The directory of the manifest
                root: The reference to the root of the scan
                manifest: The manifest object
        """

        self.log('Creating manifest for ' + dir, COLORS['GREEN'])
        f = open(os.path.join(root, dir , 'manifest.json'),'w+')
        f.write(json.dumps(manifest))
        f.close()
        self.log('Manifest completed!')


class ManifestBuilderSettings(object):

    """
    Builds the settings object to be given to the main program

    Args:
        arguments: The arguments passed to the program
    """

    dir=""

    def __init__(self, arguments=[]):

        #TODO(fed135): Make this smarter. Need better detection of the
        #    directory parameter
        self.dir = arguments[1]

        for x in OPTIONS:
            setattr(self, OPTIONS[x], (x in arguments))


def main():

    """
    Entry point.
    Builds the config object from the command line parameters
    then passes it to the ManifestBuilder class

    """

    settings = ManifestBuilderSettings(sys.argv)
    ManifestBuilder(settings)


if __name__ == '__main__':
    main()
