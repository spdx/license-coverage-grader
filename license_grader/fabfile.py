
"""
Fabric file to standardize our dev process.
1. Run the dev setup with: $ fab debug. For postgres. fab debug:psql
2. Run the prod setup with: $ fab prod. For postgres. fab prod:psql
3. Remember to stop the servers, with $ fab stop

All Rights Reserved. Hadron Tech LLC 2016.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from contextlib import contextmanager, nested
import os
import platform
import sys
import time
from fabric.api import env, local, task, warn_only
from colorama import Back, Fore, Style, init
# Launch tasks here.

IS_WIN = platform.system().lower().startswith("win")

IS_TTY = sys.stdout.isatty()

STATUS_MARK = u'\u2712' * IS_TTY
X_MARK = u'\u2718' * IS_TTY
CHECK_MARK = u'\u2714' * IS_TTY
WARNING_MARK = u"\u26A0" * IS_TTY
NOTE_MARK = u'\u2710' * IS_TTY

def W(string, prefix=" "):
    """Returns "" if this platform is WIN."""
    return "" if IS_WIN else prefix + string

def _fprint(bg, status, message):
    print(Fore.WHITE + Style.BRIGHT + bg + " " + status + " ", end="")
    print(Fore.WHITE + Style.BRIGHT + " " + message)


def warn(message):
    _fprint(Back.BLACK, "WARNING", message + W(Fore.YELLOW + WARNING_MARK))


def success(message):
    _fprint(Back.BLACK, "SUCCESS", message + W(Fore.GREEN + CHECK_MARK))


def note(message):
    _fprint(Back.BLACK, " NOTE  ", message + W(Fore.CYAN + NOTE_MARK))


def error(message):
    _fprint(Back.BLACK, " ERROR ", message + W(Fore.RED + X_MARK))


@contextmanager
def introduce(what):
    """Status decorate an event."""
    start_time = time.time()
    introducer_dict = {}

    def timer():
        return str(time.time() - start_time) + " seconds"

    print(Fore.WHITE + Back.BLACK + Style.BRIGHT + "  START  ", end="")
    print(Fore.WHITE + Style.BRIGHT + W(STATUS_MARK) + " " + what)
    try:
        yield introducer_dict
    except:
        error(what + timer())
        raise  # let fabric handle this.
    else:
        if not introducer_dict:
            success(what + timer())
        else:
            warn(what + timer())

@task
def setup():
    # Setups the project, installs the necessary utilities so that commands do not fail
    """Setup the project"""
    with introduce("Checking Cloc installation: "):
        local('sudo apt-get install cloc')
    with introduce("Checking and installing requriements: "):
        local('pip install -r requirements.txt')

@task
def hello(who="world"):
    """Hello world"""
    print("Hello {who}!".format(who=who))

@task
def analyse(package=""):
    """Analyse a source file package"""
    with introduce("Analysing the source package: "):
        setup()
        cloc_command_result = local('cloc --xml {package}'.format(package=package), capture=True)
        print(cloc_command_result)
