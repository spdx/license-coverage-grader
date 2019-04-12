# SPDX-License-Identifer: Apache-2.0


from setuptools import setup


def readme():
<<<<<<< HEAD
    with open('.github/README.md') as f:
=======
    """Opens and reads the readme file"""
    with open('README.md') as f:
>>>>>>> Adding description to setup.py file
        return f.read()


setup(
<<<<<<< HEAD
    name="License Coverage Grader",
    long_description=readme(),
    version='0.1',
    py_modules=['lcg_commands'],
    author='Nuvadga Christian Tete',
    author_email='tetechris20@gmail.com',
    description='SPDX Utility to grade License information',
=======
    name="License Coverage Grader", # Package name
    long_description=readme(), # Package description and documentation
    version='0.1', # Package version
    py_modules=['cmds'], # Python modules installed
    author='Nuvadga Christian Tete', # Source code author
    author_email='tetechris20@gmail.com', # Source code email author
    description='SPDX Utility to grade License information', # Brief description of package
>>>>>>> Adding description to setup.py file
    install_requires=[
        'Click',
        'xmlbuilder',
        'Fabric',
        'lxml',
        'colorama',
        'python-Levenshtein'
    ], # Required python packages for the utility to run smoothly
    entry_points={
<<<<<<< HEAD
        'console_scripts': ['spdx-coverage-scan=lcg_commands:scan',
                            'spdx-coverage-analyse=lcg_commands:analyse',
                            'spdx-coverage-check=lcg_commands:check',
                            'spdx-coverage-grade=lcg_commands:grade'],
    }
=======
        'console_scripts': ['scan=cmds:scan',
                            'analyse=cmds:analyse',
                            'check=cmds:check',
                            'grade=cmds:grade'],
    } # Commands shipped with this utility
>>>>>>> Adding description to setup.py file
)
