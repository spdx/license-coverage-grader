from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name="License Coverage Grader",
    long_description=readme(),
    version='0.1',
    py_modules=['cmds'],
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
        'console_scripts': ['myhello=cmds:cli',
                            'scan=cmds:scan',
                            'analyse=cmds:analyse',
                            'check=cmds:check',
                            'grade=cmds:grade'],
    }
)
