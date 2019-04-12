
# Copyright (c) 2017 Nuvadga Christian. All rights reserved.
# https://github.com/spdx/license-coverage-grader/
# The License-Coverage-Grader software is licensed under the Apache License version 2.0.
# Data generated with license-coverage-grader require an acknowledgment.
# license-coverage-grader is a trademark of The Software Package Data
# Exchange(SPDX).

# You may not use this software except in compliance with the License.
# You may obtain a copy of the License at: http://apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

# When you publish or redistribute any data created with license-coverage-grader or any license-coverage-grader
# derivative work, you must accompany this data with the following
# acknowledgment:

#   Generated with license-coverage-grader and provided on an "AS IS" BASIS, WITHOUT WARRANTIES
#   OR CONDITIONS OF ANY KIND, either express or implied.

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
