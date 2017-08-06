import argparse
import sys

from twostack_interpreter import TwoStackInterpreter

def main():
    '''The main entrypoint for the interpreter running on the terminal.'''
    interpreter = TwoStackInterpreter()

    if len(sys.argv) >= 2:
        interpreter.execute_file(sys.argv[1])
    # TODO: work out a scheme for printing help

if __name__ == '__main__':
    main()
