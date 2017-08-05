'''TwoStack
Author: Jesse Sheehan <jesse@sheehan.nz>

TODO: Show command line arguments, etc...
'''

import sys
import re

from twostack_feature_provider import TwoStackFeatureProvider

class TwoStackInterpreter(TwoStackFeatureProvider):
    '''The formal interpreter for TwoStack.'''

    def reset(self):
        '''Resets the interpreter state.'''
        self.program = ''
        self.loop = {}
        self.index = 0
        self.stack = []
        self.ztack = []
        self.store = {}
        self.callstack = []

    def debug(self):
        '''Presents the debug menu to the user.'''
        prompt = 'Debug: ((c)ontinue, (s)tack, (z)tack, (a)liases, (q)uit) > '
        while True:
            char = input(prompt)
            if char == 'c':
                return
            elif char == 'a':
                self.print_aliases()
            elif char == 's':
                self.print_stack()
            elif char == 'z':
                self.print_ztack()
            elif char == 'q':
                sys.exit()
            else:
                print('unknown command')

    def print_stack(self):
        '''Prints the stack to the terminal.'''
        print('Stack: ')
        for i in range(len(self.stack)):
            print('  {}: {}'.format(i, self.stack[i]))

    def print_ztack(self):
        '''Prints the ztack to the terminal.'''
        print('Ztack: ')
        for i in range(len(self.ztack)):
            print('  {}: {}'.format(i, self.ztack[i]))

    def print_aliases(self):
        '''Print the aliases to the terminal.'''
        print('Aliases: ')
        for alias, value in self.store.items():
            print('  {}: {}'.format(alias, value))

    def error(self, message):
        '''Prints detailed error information to the terminal.'''
        newline = '\n'

        # specifies the number amount of context characters to provide
        padding = 40

        source_start = max(0, self.index - padding)

        start_newline = self.program.rfind(newline, source_start, self.index)

        if start_newline > -1:
            source_start = max(start_newline + 1, source_start)

        source_end = min(len(self.program), self.index + padding)

        end_newline = self.program.find(newline, self.index, source_end)

        if end_newline > -1:
            source_end = min(source_end, end_newline)

        line = self.program[:self.index].count(newline) + 1
        column = self.index - source_start + 1

        print(self.program[source_start:source_end])
        print((' ' * (column - 1)) + '^')

        print('error: {} on line {}, column {}'.format(message, line, column))

    def execute_file(self, filename):
        '''Executes a file through the interpreter.'''
        try:
            with open(filename) as file:
                program = file.read()
                self.execute(program)
        except:
            print('An unexpected error occurred')
            raise

    def execute(self, program):
        '''Execute a string.'''
        self.program = program

        while self.index < len(program):
            rest = program[self.index:]
            extra_advance = None
            cmd = None

            # check for 2 character operators
            if rest[:2] in self.commands.keys():
                cmd = self.commands[rest[:2]]

            # check for 1 character operators
            elif rest[0] in self.commands.keys():
                cmd = self.commands[rest[0]]

            # check for regular expressions
            else:
                for key in self.commands:
                    this_cmd = self.commands[key]
                    if this_cmd.get('is_regex', False):
                        if re.match(key, rest):
                            cmd = this_cmd
                            break

            if cmd is not None:
                if len(self.stack) >= cmd['min']:
                    extra_advance = cmd['function']()
                else:
                    self.error('not enough elements on the stack')
                    break

            elif rest[0] == '_':
                self.debug()

            else:
                self.error('unknown symbol \'{}\''.format(rest[0]))
                break

            if extra_advance is None:
                extra_advance = 0

            self.index += 1 + extra_advance

def main():
    '''The main entrypoint for the interpreter running on the terminal.'''
    interpreter = TwoStackInterpreter()

    if len(sys.argv) >= 2:
        interpreter.execute_file(sys.argv[1])
    # TODO: work out a scheme for printing help

if __name__ == '__main__':
    main()
