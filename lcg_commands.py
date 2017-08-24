
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

import click
from utils import AnalysePackage, ScanSpdx, CheckPackage, GradePackage


@click.command()
@click.option('--verbose', is_flag=True, help="Will print verbose messages.")
@click.option('--spdx', multiple=False, default='', help='The spdx file.')
def scan(verbose, spdx):
    """Scans an spdx document"""
    if verbose:
        click.echo("We are in the verbose mode.")
    click.echo("Scanning the spdx document.")
    scan_obj = ScanSpdx(spdx)
    scan_obj.scan()
    click.echo('Scanned the file: {0}'.format(spdx))


@click.command()
@click.option('--verbose', is_flag=True, help="Will print verbose messages.")
@click.option(
    '--package',
    multiple=False,
    default='',
    help='The source package.')
@click.option('--lines', multiple=False, default='',
              help='The min number of code lines allowed.')
def analyse(verbose, package, lines):
    """Analyse a source package"""
    if verbose:
        click.echo("We are in the verbose mode.")
    click.echo("Analysing the source package.")
    analyse_obj = AnalysePackage(package, lines)
    analyse_obj.analyse()
    click.echo('Analysed the package {0}'.format(package))


@click.command()
@click.option('--verbose', is_flag=True, help="Will print verbose messages.")
@click.option('--spdx', multiple=False, default='', help='The spdx document.')
@click.option(
    '--package',
    multiple=False,
    default='',
    help='The source package.')
@click.option('--lines', multiple=False, default=0,
              help='The min number of code lines allowed.')
@click.option('--percent', multiple=False, default=0,
              help='The min matching percentage.')
def check(verbose, spdx, package, lines, percent):
    """Checks the compatibility between an spdx document and a source package."""
    if verbose:
        click.echo("We are in the verbose mode.")
    click.echo(
        "We are now checking the source package/spdx document compatibility.")
    check_obj = CheckPackage(spdx, package, lines, percent)
    check_obj.check()
    click.echo("Checked the source package/spdx document compatibility.")


@click.command()
@click.option('--verbose', is_flag=True, help="Will print verbose messages.")
@click.option('--spdx', multiple=False, default='', help='The spdx document.')
@click.option(
    '--package',
    multiple=False,
    default='',
    help='The source package.')
@click.option('--lines', multiple=False, default=0,
              help='The min number of code lines allowed.')
@click.option('--percent', multiple=False, default=0,
              help='The min matching percentage.')
def grade(verbose, spdx, package, lines, percent):
    """Grades a source package"""
    if verbose:
        click.echo("We are in the verbose mode.")
    click.echo("Grading the source package.")
    grade_obj = GradePackage(spdx, package, lines, percent)
    grade_results = grade_obj.grade()
    #click.echo("Source package was successfull graded against its spdx document.")
