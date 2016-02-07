"""
pypi-up a simple command line tool to increase version number of package
and release on Pypi. Also Git Tag/Push the release.

It can increase patch, minor, major, release and dev version

Features:
    - Increase versionning 
    - Git Tag/Push release
    - Release to PYPI

Setup:

run: pypi-up --setup 

Manually:

Edit 'setup.cfg' at the root of your package and must have the following line

[pypi-up]
version-file = "__about__.py"


The about file must contain a variable: `__version__`

__version__ = "1.2.4"

What it will do, it will access the file and change the version number


"""
import re
import os
import argparse
import ConfigParser
from reversionup import Reversionup
import sh

__NAME__ = "pypi-up"
__version__ = "0.0.1"

CWD = os.getcwd()
setup_cfg = "%s/setup.cfg" % CWD
about_file = "%s/__about__.py" % CWD
conf_section_name = "pypi-up"

about_file_content = '''
""" __about__ """

__all__ = [
    "__title__", "__summary__", "__uri__", "__version__", "__author__",
    "__email__", "__license__", "__copyright__",
]

__title__ = ""
__version__ = "0.0.0"
__summary__ = ""
__uri__ = ""
__author__ = ""
__email__ = ""
__license__ = ""
__copyright__ = "(c) 2016 %s" % __author__
'''


def replace_in_file(file, pattern, replacement):
    with open(file, "r+") as f:
        c = re.sub(pattern, replacement, f.read())
        f.seek(0)
        f.truncate()
        f.write(c)


def replace_file_version(file, version):
    pattern = r'__version__\s*=\s*"([\d.\w\-]+)"'
    repl = "__version__ = \"%s\"" % version
    replace_in_file(file, pattern, repl)


def main():

    try:
        prog = "pypi-up"
        desc = "%s %s" % (__NAME__, __version__)
        desc += " - pypi-up a simple command line tool to increase version number of package" \
                "and release on Pypi. Also Git Tag/Push the release"

        parser = argparse.ArgumentParser(prog=prog,
                                         description=desc)
        parser.add_argument("--setup",
                           help="Setup PYPI-REL",
                           action="store_true")        
        parser.add_argument("-v", "--version",
                           help="Show the current version",
                           action="store_true")
        parser.add_argument("-p", "--patch",
                           help="Increment PATCH version",
                           action="store_true")
        parser.add_argument("-m", "--minor",
                           help="Increment MINOR version and reset patch",
                           action="store_true")
        parser.add_argument("-j", "--major",
                           help="Increment MAJOR version and reset minor and patch",
                           action="store_true")
        parser.add_argument("-e", "--edit",
                           help="Manually enter the version number to bump",
                           action="store")
        parser.add_argument("--dry",
                           help="DRY RUN. To test the release, but it will not make any changes",
                           action="store_true")
        parser.add_argument("-x", "--skip-prompt",
                           help="Skip prompt",
                           action="store_true")
        arg = parser.parse_args()
        config = ConfigParser.ConfigParser()
        
        print("-" * 80)
        print("=== PYPI Up ===")
        print("")
        
        if arg.setup:
            print("Setting up...")
            if not os.path.isfile(about_file):
                with open(about_file, "w+") as f:
                    f.write(about_file_content)
            if not os.path.isfile(setup_cfg):
                config.add_section(conf_section_name)
                config.set(conf_section_name, "version-file", "__about__.py")
                with open(setup_cfg, "w+") as f:
                    config.write(f)
            print("Done!")
            print("-" * 80)
            exit()
        
        
        with sh.pushd(CWD):
            if sh.git("status", "--porcelain").strip():
                raise Exception("Repository is UNCLEAN. Commit your changes")

            config.read(setup_cfg)
            version_file = config.get(conf_section_name, "version-file")
            version_file = os.path.join(CWD, version_file)
            if not os.path.isfile(version_file):
                raise Exception("version-file '%s' is required" % version_file)

            rvnup = Reversionup(file=setup_cfg)
            old_version = rvnup.version

            if arg.edit:
                rvnup.version = arg.edit
            elif arg.patch:
                rvnup.inc_patch()
            elif arg.minor:
                rvnup.inc_minor()
            elif arg.major:
                rvnup.inc_major()
            elif arg.version:
                print("Current version: %s" % rvnup.version)
                print("-" * 80)
                exit()

            if arg.dry:
                print("** DRY RUNNING **")
                print("")

            print("* New version: %s " % rvnup.version)
            print("Old version: %s" % old_version)
            print("")

            if not arg.skip_prompt \
                    and raw_input("Continue with the release? (y | n) ").strip() == "n":
                print("** Release Aborted")
                print("-" * 80)
                exit()

            skip_tag = not arg.skip_prompt \
                       and raw_input("Git Tag/Push release version? (y | n) ").strip().lower() == "n"
            skip_pypi = not arg.skip_prompt \
                        and raw_input("Release to PYPI? (y | n) ").strip().lower() == "n"

            print("")

            if not arg.dry:
                rvnup.write()
                replace_file_version(version_file, rvnup.version)

            if arg.dry or skip_tag:
                print("- Git Tag/Push release: skipped")
            else:
                tag_name = "v%s" % rvnup.version
                print("+ Git Tag release version: %s " % tag_name)
                sh.git("add", ".")
                sh.git("commit", "-m", "Tagged release: %s" % tag_name)
                sh.git("tag", "-a", tag_name, "-m", tag_name)
                print("+ Git Push release to repo ...")
                sh.git("push", "origin", "master")
                sh.git("push", "--tags")

            if arg.dry or skip_pypi:
                print("- Release to Pypi: skipped")
            else:
                print("+ Releasing to PYPI ...")
                sh.python("setup.py", "register", "-r", "pypi")
                sh.python("setup.py", "sdist", "upload", "-r", "pypi")

        print("-" * 80)
        print("")

    except Exception as ex:
        print("Error: %s" % ex.message)
        exit(1)
