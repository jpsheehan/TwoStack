'''TwoStack
Author: Jesse Sheehan <jesse@sheehan.nz>

TODO: Show command line arguments, etc...
'''

import sys

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
        for a, v in self.store.items():
            print('  {}: {}'.format(a, v))

    def error(self, message):
        '''Prints detailed error information to the terminal.'''
        line = self.program[:self.index].count('\n') + 1
        column = self.program[:self.index].rfind('\n') - self.index
        # TODO: fix column calculation

        source_start = max(0, self.index - 10)
        source_start = max(self.program.rfind('\n', source_start, self.index) + 1, source_start)

        source_end = min(len(self.program) - 1, self.index + 10)
        source_end = min(source_end, self.program.find('\n', self.index, source_end))

        source_offset = self.index - source_start

        print(self.program[source_start:source_end])
        print((' ' * source_offset) + '^')

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

            if rest[:2] in self.commands.keys():
                cmd = self.commands[rest[:2]]
            elif rest[0] in self.commands.keys():
                cmd = self.commands[rest[0]]
            else:
                cmd = None

            if cmd is not None:
                if len(self.stack) >= cmd['min']:
                    extra_advance = cmd['function']()
                else:
                    self.error('not enough elements on the stack')
                    break

            elif rest[0].isdigit():
                # shim to get integer literals working
                extra_advance = self.op_intliteral()

            elif rest[0].isalpha():
                # shim to get alias recollection without any leading symbols
                extra_advance = self.op_aliasrecall()

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

if __name__ == '__main__':
    main()
