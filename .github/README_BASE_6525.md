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

`pip install --editable . `

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

### 1- Spdx document scan
if you have install the project with pip;
`scan --spdx ~/path/doc.spdx`
Scans the spdx document, and outputs the results in an xml format as a string, on the terminal. These results are not printed to a file.
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

### 2- Package analysis
if you have install the project with pip;
`analyse --package ~/path_to_source_package`
Analyses the package it receives, and outputs the analysis results in an xml format as a string, on the terminal.
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

### 3- Check
if you have install the project with pip;
`check --spdx ~/path_to_spdx_document --package ~/path_to_source_package --lines 0 --percent 0`
This Scans the pdx document and analyses the source package to determine how compatible they are.


### 4- Grader
if you have install the project with pip;
`grade --spdx ~/path_to_spdx_document --package ~/path_to_source_package --lines 0 --percent 0`
This runs the package analysis and the spdx file scan commands described above, but does not output any other result appart from the license coverage grade attributed to the package; as show below:
```
The package matches the spdx file by 0.0, the lowest permitted value is: 0
Preliminary scan as established a match between the spdx document and the source files. Proceeding ...
GRADE:  F with 0.0 %  pass for files_with_license_concluded
GRADE:  F with 0.0 %  pass for files_with_any_kind_of_license_infos


```
