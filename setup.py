from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='license-coverage-grader',
      long_description=readme(),
      version='0.1',
      description='SPDX Utility to grade License information',
      url='https://github.com/krysnuvadga/license-coverage-grader',
      author='Nuvadga Christian Tete',
      author_email='tetechris20@gmail.com',
      license='MIT',
      packages=['license_grader'],
      zip_safe=False,
      entry_points = {
        'console_scripts': ['lcg_main=license_grader.command_line:main',
                            'lcg_scan=license_grader.command_line:scan',
                            'lcg_analyse=license_grader.command_line:analyse',
                            'lcg_grade=license_grader.command_line:grade',
                            'lcg_check=license_grader.command_line:check',
                            'lcg_setup=license_grader.command_line:setup'],
    })
