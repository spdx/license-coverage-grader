from setuptools import setup

def readme():
    with open('.github/README.md') as f:
        return f.read()

setup(
    name="License Coverage Grader",
    long_description=readme(),
    version='0.1',
    py_modules=['lcg_commands'],
    author='Nuvadga Christian Tete',
    author_email='tetechris20@gmail.com',
    description='SPDX Utility to grade License information',
    install_requires=[
        'Click',
        'xmlbuilder',
        'Fabric',
        'lxml',
        'colorama',
        'python-Levenshtein'
    ],
    entry_points={
        'console_scripts': ['spdx-coverage-scan=lcg_commands:scan',
                            'spdx-coverage-analyse=lcg_commands:analyse',
                            'spdx-coverage-check=lcg_commands:check',
                            'spdx-coverage-grade=lcg_commands:grade'],
    }
)
