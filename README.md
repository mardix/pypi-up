#PYPI-UP


A tool to release package on Pypi, by incrementing the version number. 
It also git tag the version and push it to the repository.

##### Requirements:
- git 

## Installation and setup

    pip-install pypi-up
    
    pypi-up --setup
    
## CLI

### Release the current version 

    pypi-up 
    
follow the prompt

### Increment version and release

#### Increase the patch number 

    pypi-up -p

    > 0.0.1
    
    
#### Increase the minor number 

    pypi-up -m

    > 0.1.0
    

#### Increase the major number 

    pypi-up -j

    > 1.0.0
    
#### Manually changed the number 

    pypi-up -e 1.2.3

    > 1.2.3
    
#### Dry Run 

If you want to test the release process, you can do a dry run

    pypi-up --dry
    
### Skip prompt 

To skip the prompt

    pypi-up -x
    
---

### setup.cfg and __about__.py 

**setup.cfg** is a config file that host the version number and the pypi-up file to update.

**__about__.py** contains the package's info. `__version__` is required to be included 
in the file.

With these two file, `pypi-up` will be able to increase the version and update the 
__about__.py effortlessly. 

By the default the __about__.py is at the root of the directory.

But if you want to place it somewhere else, in your `setup.cfg` change the following to your path

    # setup.cfg
    
    [pypi-up]
    version-file = $path/__about__.py  

---

License: MIT

(c) Copyright 2016 Mardix

    