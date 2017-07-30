import license_grader
import sys, argparse, logging
from fabfile import scan, check, grade, analyse, setup


# Gather our code in a main() function
def argument_checker(argument_list, number_expected):
    number_given = len(argument_list)
    if number_given != (number_expected+1):
        print("Sorry, this command takes {} arguments, you passed {}.".format(number_expected, number_given))
        return False
    return True


def main():
    print "Hello there."


def lcg_check():
    if argument_checker(sys.argv, 3):
        check(spdx_file=sys.argv[1], package=sys.argv[2], min_code_lines=sys.argv[3], run_setup=True)
    print license_grader.text()


def lcg_setup():
    setup()
    print license_grader.text()


def lcg_scan():
    if argument_checker(sys.argv, 1):
        scan(spdx_file=sys.argv[1], run_setup=True)
    print license_grader.text()


def lcg_analyse():
    if argument_checker(sys.argv, 2):
        analyse(package=sys.argv[1], min_code_lines=sys.argv[2])
    print license_grader.text()


def lcg_grade():
    if argument_checker(sys.argv, 3):
        grade(spdx_file=sys.argv[1], package=sys.argv[2], min_code_lines=sys.argv[3])
    print license_grader.text()
