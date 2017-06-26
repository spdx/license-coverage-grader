# license-coverage-grader
This is a tool which take an SPDX document and pointer to the original source files, and determine a "grade" score to quantify how complete the licensing information is at the file level for the code represented by the SPDX document.

## Project setup
Ideal OS: Ubuntu 16.04 LTS

### 1- The virtual environment we use for this repo is virtualenv.
create a folder named "license-grader-env"(you can call this folder anything you want, but this is cleaner), and navigate to it.

`mkdir license-grader-env && cd license-grader-env`

### 2- Make that folder a virtual environment

`virtualenv .`

### 3- Clone the repository

`git clone https://github.com/krysnuvadga/license-coverage-grader.git`

### 4- Navigate to the project you just cloned

`cd license-coverage-grader`

### 5- go to license_grader

`cd license_grader`

By now, your path in the terminal should look like:

`license-grader-env/license-coverage-grader/license_grader$ `

### 6- Activate the virtual environment.

`source ../../bin/activate`

### 7- Now, install all dependencies, using pip.
The dependencies are listed in the requirements file.
Install them by running:

`pip install -r requirements.txt`

This is just for safety, because before each command of the project is run (spdx document scan or pacakge analysis), these requirements are checked for installation if need be.
So, one could skip this step and start using the project right away.


