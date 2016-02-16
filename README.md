# manifest-builder

Allows you to scan a folder structure and generate one global 
manifest, or multiple ones in each folder. 
  
  
## Running

    $ python manifestBuilder.py [target_folder] [options]
    

## Options

    -a    file paths will be absolute instead of relative
    -d    includes directories in the manifest
    -l    will output a local manifest in each folder instead of a global one
    -s    adds file size in the manifest (bytes)
    -v    verbose mode
      
      
## Roadmap

- Make verbose output more detailed
- Add filtering option for specific file types/file names, etc.
- Add option to change output file name/location
- Add help method
