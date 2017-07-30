import license_grader
import sys, argparse, logging


# Gather our code in a main() function
def argument_checker(argument_list, number_expected):
    number_given = len(argument_list)
    if number_given != number_expected:
        print("Sorry, this command takes {} arguments, you passed {}.".format(number_expected, number_given))
        return False
    return True


def main():
    print "Hello there."


def check():
    argument_checker(sys.argv, 3)
    print license_grader.text()


def setup():
    print license_grader.text()


def scan():
    argument_checker(sys.argv, 1)
    print license_grader.text()


def analyse():
    argument_checker(sys.argv, 2)
    print license_grader.text()


def grade():
    argument_checker(sys.argv, 3)
    print license_grader.text()
