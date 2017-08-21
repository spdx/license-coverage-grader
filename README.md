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

`git clone https://github.com/spdx/license-coverage-grader.git`

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

### 8- Install the project with pip.
Change the directory back to the project root,
`cd ..`
By now, you should be at:
`license-grader-env/license-coverage-grader` , with the virtual environment activated.

This will give you access to a whole new lot of `non fab` commands, as described below.

## Available terminal commands / functions

Requirement:
Inorder to run the commands listed below, 
### i) you should be in the path:
`license-grader-env/license-coverage-grader/license_grader$ `

### ii) You must have the virtualenv activated:
If in `license-grader-env/license-coverage-grader/license_grader$ ` , 
Run `source ../../bin/activate`

### 1- Setup
`fab setup`
Installs cloc and requirements. However, since fabric is a requirement itself, this cannot be run without fabric being installed, reason why, for the first run; you should run `pip install -r requirements.txt` yourself.

### 2- Spdx document scan
if you have install the project with pip;
`lcg_scan:~/path/doc.spdx`
else;
`fab scan:~/path/doc.spdx`
`
Scans the spdx document, and outputs the results in an xml format as a string, on the terminal. These results are not printed to a file. Before this is run, the command `fab setup` mentioned above will be run, to ascertain that we would not have errors due to the absence of cloc, or any dependencies.
An example output is shown below:
```<?xml version="1.0" encoding="utf-8" ?>
    <spdx_file>
      <data>
          <item>
              <file val="src/lib/Makefile" />
              <license_info val="LINFO-1 LINFO-2" />
              <license_concluded val="LICO-1 LICO-2" />
          </item>
          <item>
              <file val="src/pkgagent/agent_tests/testdata/fossology-1.2.0-1.el5.i386.rpm/etc/init.d/fossology" />
              <license_info val="NOASSERTION" />
              <license_concluded val="NOASSERTION" />
          </item>
          <item>
              <file val="src/testing/dataFiles/TestData/archives/fossI16L518.7z/fossology/agents/foss_license_agent/licinspect/Makefile" />
              <license_info val="NOASSERTION" />
              <license_concluded val="NOASSERTION" />
          </item>
      </data>
  </spdx_file>
```

### 3- Package analysis
if you have install the project with pip;
`lcg_analyse:~/path_to_source_package`
else;
`fab analyse:~/path_to_source_package`
Analyses the package it receives, and outputs the analysis results in an xml format as a string, on the terminal. Before this is run, the command `fab setup` mentioned above will be run, to ascertain that we would not have errors due to the absence of cloc, or any dependencies.
An example output is shown below:
```
<?xml version="1.0"?><results>
<header>
  <cloc_url>http://cloc.sourceforge.net</cloc_url>
  <cloc_version>1.60</cloc_version>
  <elapsed_seconds>7.50479102134705</elapsed_seconds>
  <n_files>733</n_files>
  <n_lines>134231</n_lines>
  <files_per_second>97.6709408583149</files_per_second>
  <lines_per_second>17886.0410127592</lines_per_second>
</header>
<files>
  <file name="cadasta-platform/functional_tests/pages/Registration.py" blank="18" comment="2" code="64"  language="Python" />
  <file name="cadasta-platform/cadasta/templates/allauth/account/email.html" blank="21" comment="0" code="64"  language="HTML" />
  <file name="cadasta-platform/cadasta/questionnaires/views/api.py" blank="16" comment="0" code="64"  language="Python" />
  <file name="cadasta-platform/cadasta/party/urls/default.py" blank="6" comment="0" code="64"  language="Python" />
</files>
</results>
Analysing the source package: 3.90155696869 seconds

Done.
```
### 4- Grader
if you have install the project with pip;
`lcg_grade:~/path_to_spdx_document,~/path_to_source_package,min_code_lines`
else;
`fab grade:~/path_to_spdx_document,~/path_to_source_package,min_code_lines`
This runs the package analysis and the spdx file scan commands described above, but does not output any other result appart from the license coverage grade attributed to the package; as show below:
```
GOOD! SPDX DOCUMENT IS POINTING TO ITS ORIGINAL SOURCE PACKAGE.

GRADE:  A with 99.3732590529 %  pass for files_with_license_concluded
Analyse and Scan: 1290.17038298 seconds

Done.

```
