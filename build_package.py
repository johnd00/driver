import re
import sys
import os
import subprocess

packages = ['admintools', 'nodetools']


def get_version(pkg=None):
    try:
        f = open('%s/%s/__init__.py' % (pkg, pkg), 'r')
        lines = f.readlines()

        for line in lines:
            if re.match(r'^__version', line):
                version = line.split('=')[1].strip()
                version = version.replace('"', '').strip()
        return version
    except:
        return None
    finally:
        f.close()


def update_version(pkg=None, ver=None):
    try:
        f = open('%s/%s/__init__.py' % (pkg, pkg), 'r')
        lines = f.readlines()
    except:
        return -1
    finally:
        f.close()

    try:
        f = open('%s/%s/__init__.py' % (pkg, pkg), 'w')
        for line in lines:
            if re.match(r'^__version', line):
                f.write('__version__ = "%s"\n' % ver)
            else:
                f.write(line)
    except:
        return -1
    finally:
        f.close()


def clean_dist(pkg=None):
    command = 'sudo rm -r ./%s/deb_dist/*' % pkg
    output = subprocess.Popen(command,
                              shell=True,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
    out, err = output.communicate()
    return output.returncode


def build_python_package(pkg=None):
    version = get_version(pkg)
    if version is not None:
        print('\n')
        print 'Current %s version is %s' % (pkg, version)
        new_version = raw_input('Enter new version number ----> ')
    update_version(pkg, new_version)

    clean_dist(pkg)

    print 'building %s version %s....' % (pkg, new_version)
    os.chdir(pkg)
    command = 'sudo make package'
    output = subprocess.Popen(command,
                              shell=True,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
    out, err = output.communicate()
    os.chdir('..')
    return output.returncode


def main():
    if len(sys.argv) == 1:
        print 'please specify a package to build'
        return -1
    package = sys.argv[1]
    if package == 'all':
        for p in packages:
            build_python_package(p)
    else:
        build_python_package(package)

if __name__ == '__main__':
    main()
