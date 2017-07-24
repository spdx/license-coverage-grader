from xml.dom.minidom import parse, parseString
import xml.dom.minidom
from xmlbuilder import XMLBuilder

from .views import get_xml_item_count, get_xml_item_value, code_line_validator, parse_xml_results, grade_scale, compute_grade, get_number_of_common_files, establish_link, VALUES_TO_AVOID

COMPLETE_XML_STRING = """<spdx_file>
    <data>
        <item>
            <file val="Tool 10571"/>
            <license_info val="spxd2:67"/>
            <license_concluded val="Match"/>
        </item>
        <item>
            <file val="Makefile.process"/>
            <license_info val="NOASSERTION"/>
            <license_concluded val="NOASSERTION"/>
        </item>
        <item>
            <file val="src/cli/fossjobs.pod"/>
            <license_info val="NOASSERTION"/>
            <license_concluded val="NOASSERTION"/>
        </item>
        <item>
            <file val="src/cli/tests/duplicate-Upfolder.php"/>
            <license_info val="GPL-2.0"/>
            <license_concluded val="GPL-2.0"/>
        </item>
        <item>
            <file val="src/copyright/agent_tests/testdata/testdata26"/>
            <license_info val="FTL"/>
            <license_concluded val="NOASSERTION"/>
        </item>
        <item>
            <file val="src/copyright/ui/ecc-hist.php"/>
            <license_info val="GPL-2.0"/>
            <license_concluded val="GPL-2.0"/>
        </item>
        <item>
            <file val="src/lib/Makefile"/>
            <license_info val="LINFO-1 LINFO-2"/>
            <license_concluded val="LICO-1 LICO-2"/>
        </item>
        <item>
            <file val="src/testing/dataFiles/TestData/archives/fossI16L518.7z/fossology/agents/foss_license_agent/Licenses/MkCache"/>
            <license_info val="NOASSERTION"/>
            <license_concluded val="NOASSERTION"/>
        </item>
        <item>
            <file val="src/testing/dataFiles/TestData/archives/fossI16L518.7z/fossology/agents/foss_license_agent/bSAM/Makefile"/>
            <license_info val="LicenseRef-BSD"/>
            <license_concluded val="GPL-2.0"/>
        </item>
    </data>
<results>
<header>
  <cloc_url>http://cloc.sourceforge.net</cloc_url>
  <cloc_version>1.60</cloc_version>
  <elapsed_seconds>0.0336780548095703</elapsed_seconds>
  <n_files>6</n_files>
  <n_lines>172</n_lines>
  <files_per_second>178.157557909045</files_per_second>
  <lines_per_second>5107.18332672594</lines_per_second>
</header>
<files>
  <file name="/home/mikael/Desktop/S/talent_env/talent_mgr/talent_mgr_core/views.py" blank="9" comment="1" code="21" language="Python"/>
  <file name="/home/mikael/Desktop/S/talent_env/talent_mgr/talent_mgr_core/urls.py" blank="1" comment="0" code="9" language="Python"/>
  <file name="/home/mikael/Desktop/S/talent_env/talent_mgr/talent_mgr_core/apps.py" blank="3" comment="1" code="4" language="Python"/>
  <file name="/home/mikael/Desktop/S/talent_env/talent_mgr/talent_mgr_core/admin.py" blank="2" comment="2" code="2" language="Python"/>
  <file name="/home/mikael/Desktop/S/talent_env/talent_mgr/talent_mgr_core/tests.py" blank="2" comment="2" code="2" language="Python"/>
  <file name="/home/mikael/Desktop/S/talent_env/talent_mgr/talent_mgr_core/models.py" blank="0" comment="111" code="0" language="Python"/>
  <total blank="17" comment="117" code="38"/>
</files>
</results></spdx_file>"""


COMPLETE_XML_STRING_2 = """<spdx_file>
    <data>
        <item>
            <file val="Tool 10571"/>
            <license_info val="spxd2:67"/>
            <license_concluded val="Match"/>
        </item>
        <item>
            <file val="src/copyright/ui/ecc-hist.php"/>
            <license_info val="GPL-2.0"/>
            <license_concluded val="GPL-2.0"/>
        </item>
        <item>
            <file val="src/lib/Makefile"/>
            <license_info val="LINFO-1 LINFO-2"/>
            <license_concluded val="LICO-1 LICO-2"/>
        </item>
        <item>
            <file val="src/testing/dataFiles/TestData/archives/fossI16L518.7z/fossology/agents/foss_license_agent/bSAM/Makefile"/>
            <license_info val="LicenseRef-BSD"/>
            <license_concluded val="GPL-2.0"/>
        </item>
    </data>
<results>
<header>
  <cloc_url>http://cloc.sourceforge.net</cloc_url>
  <cloc_version>1.60</cloc_version>
  <elapsed_seconds>0.0336780548095703</elapsed_seconds>
  <n_files>6</n_files>
  <n_lines>172</n_lines>
  <files_per_second>178.157557909045</files_per_second>
  <lines_per_second>5107.18332672594</lines_per_second>
</header>
<files>
  <file name="/home/mikael/Desktop/S/talent_env/talent_mgr/talent_mgr_core/views.py" blank="9" comment="1" code="21" language="Python"/>
  <file name="/home/mikael/Desktop/S/talent_env/talent_mgr/talent_mgr_core/urls.py" blank="1" comment="0" code="9" language="Python"/>
  <file name="/home/mikael/Desktop/S/talent_env/talent_mgr/talent_mgr_core/apps.py" blank="3" comment="1" code="4" language="Python"/>
  <file name="/home/mikael/Desktop/S/talent_env/talent_mgr/talent_mgr_core/admin.py" blank="2" comment="2" code="2" language="Python"/>
  <file name="/home/mikael/Desktop/S/talent_env/talent_mgr/talent_mgr_core/tests.py" blank="2" comment="2" code="2" language="Python"/>
  <file name="/home/mikael/Desktop/S/talent_env/talent_mgr/talent_mgr_core/models.py" blank="0" comment="111" code="0" language="Python"/>
  <total blank="17" comment="117" code="38"/>
</files>
</results></spdx_file>"""

SOURCE_PACKAGE_RESULTS = """<results>
<header>
  <cloc_url>http://cloc.sourceforge.net</cloc_url>
  <cloc_version>1.60</cloc_version>
  <elapsed_seconds>0.0450599193572998</elapsed_seconds>
  <n_files>6</n_files>
  <n_lines>172</n_lines>
  <files_per_second>133.15603058282</files_per_second>
  <lines_per_second>3817.13954337416</lines_per_second>
</header>
<files>
  <file name="/home/mikael/Desktop/S/talent_env/talent_mgr/talent_mgr_core/views.py" blank="9" comment="1" code="21" language="Python"/>
  <file name="/home/mikael/Desktop/S/talent_env/talent_mgr/talent_mgr_core/urls.py" blank="1" comment="0" code="9" language="Python"/>
  <file name="/home/mikael/Desktop/S/talent_env/talent_mgr/talent_mgr_core/apps.py" blank="3" comment="1" code="4" language="Python"/>
  <file name="/home/mikael/Desktop/S/talent_env/talent_mgr/talent_mgr_core/admin.py" blank="2" comment="2" code="2" language="Python"/>
  <file name="/home/mikael/Desktop/S/talent_env/talent_mgr/talent_mgr_core/tests.py" blank="2" comment="2" code="2" language="Python"/>
  <file name="/home/mikael/Desktop/S/talent_env/talent_mgr/talent_mgr_core/models.py" blank="0" comment="111" code="0" language="Python"/>
  <total blank="17" comment="117" code="38"/>
</files>
</results>"""




SPDX_SCAN_RESULTS = """<spdx_file>
    <data>
        <item>
            <file val="Tool 10571"/>
            <license_info val="spxd2:67"/>
            <license_concluded val="Match"/>
        </item>
        <item>
            <file val="Makefile.process"/>
            <license_info val="NOASSERTION"/>
            <license_concluded val="NOASSERTION"/>
        </item>
        <item>
            <file val="src/cli/foss-scheduler.pod"/>
            <license_info val="NOASSERTION"/>
            <license_concluded val="NOASSERTION"/>
        </item>
        <item>
            <file val="src/cli/fossjobs.pod"/>
            <license_info val="NOASSERTION"/>
            <license_concluded val="NOASSERTION"/>
        </item>
        <item>
            <file val="src/cli/tests/duplicate-Upfolder.php"/>
            <license_info val="GPL-2.0"/>
            <license_concluded val="GPL-2.0"/>
        </item>
        <item>
            <file val="src/copyright/agent_tests/testdata/testdata26"/>
            <license_info val="FTL"/>
            <license_concluded val="NOASSERTION"/>
        </item>
        <item>
            <file val="src/copyright/ui/ecc-hist.php"/>
            <license_info val="GPL-2.0"/>
            <license_concluded val="GPL-2.0"/>
        </item>
        <item>
            <file val="src/lib/Makefile"/>
            <license_info val="LINFO-1 LINFO-2"/>
            <license_concluded val="LICO-1 LICO-2"/>
        </item>
        <item>
            <file val="src/pkgagent/agent_tests/Unit/Makefile"/>
            <license_info val="NOASSERTION"/>
            <license_concluded val="NOASSERTION"/>
        </item>
        <item>
            <file val="src/pkgagent/agent_tests/testdata/fossology-1.2.0-1.el5.i386.rpm/etc/cron.d/fossology"/>
            <license_info val="NOASSERTION"/>
            <license_concluded val="NOASSERTION"/>
        </item>
        <item>
            <file val="src/testing/dataFiles/TestData/archives/fossI16L518.7z/fossology/agents/foss_license_agent/bSAM/Makefile"/>
            <license_info val="LicenseRef-BSD"/>
            <license_concluded val="GPL-2.0"/>
        </item>
    </data>
</spdx_file>"""

def test_get_xml_item_count_license_concluded():
    DOMTree = xml.dom.minidom.parseString(COMPLETE_XML_STRING)
    collection = DOMTree.documentElement
    assert get_xml_item_count(collection, 'license_concluded', VALUES_TO_AVOID, 'val') == 5

def test_get_xml_item_count_license_info():
    DOMTree = xml.dom.minidom.parseString(COMPLETE_XML_STRING)
    collection = DOMTree.documentElement
    DOMTree2 = xml.dom.minidom.parseString(COMPLETE_XML_STRING_2)
    collection2 = DOMTree2.documentElement
    assert get_xml_item_count(collection2, 'license_info', VALUES_TO_AVOID, 'val') == 4
    assert get_xml_item_count(collection, 'license_info', VALUES_TO_AVOID, 'val') == 6

def test_get_xml_item_value():
    sourceDOMTree = xml.dom.minidom.parseString(SOURCE_PACKAGE_RESULTS)
    source_collection = sourceDOMTree.documentElement
    assert get_xml_item_value(source_collection, 'n_files') == '6'

def test_code_line_validator():
    assert code_line_validator(SOURCE_PACKAGE_RESULTS, 0)[1] == 6
    assert code_line_validator(SOURCE_PACKAGE_RESULTS, 10)[1] == 1
    assert code_line_validator(SOURCE_PACKAGE_RESULTS, 8)[1] == 2

def test_parse_xml_results():
    assert parse_xml_results(COMPLETE_XML_STRING, 6) == (None, None)

def test_compute_grade():
    dict_of_values = {u'total_num_files_with_license': 5, u'num_license_concluded': 5, u'num_license_possible': 6, u'total_num_source_files': 6}
    assert compute_grade(dict_of_values) == (None, None)

def test_get_number_of_common_files():
    sourceDOMTree = xml.dom.minidom.parseString(SOURCE_PACKAGE_RESULTS)
    source_collection = sourceDOMTree.documentElement
    assert get_number_of_common_files(SPDX_SCAN_RESULTS, source_collection) == 0

def test_establish_link():
    assert establish_link(SPDX_SCAN_RESULTS, SOURCE_PACKAGE_RESULTS) == 0.0
