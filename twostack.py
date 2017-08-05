import sys
import os

from twostack_feature_provider import TwoStackFeatureProvider

class TwoStackInterpreter(TwoStackFeatureProvider):
    '''The formal interpreter for TwoStack.'''

    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        '''Resets the interpreter state.'''
        self.stack = []
        self.ztack = []
        self.store = {}
        self.callstack = []
        self.input = ''
        self.input_pointer = 0

    def debug(self):
        prompt = 'Debug: ((c)ontinue, (s)tack, (z)tack, (a)liases, (q)uit) > '
        while True:
            c = input(prompt)
            if c == 'c':
                return
            elif c == 'a':
                self.print_aliases()
            elif c == 's':
                self.print_stack()
            elif c == 'z':
                self.print_ztack()
            elif c == 'q':
                sys.exit()
            else:
                print('unknown command')
    
    def print_stack(self):
        print('Stack: ')
        for i in range(len(self.stack)):
            print('  {}: {}'.format(i, self.stack[i]))

    def print_ztack(self):
        print('Ztack: ')
        for i in range(len(self.ztack)):
            print('  {}: {}'.format(i, self.ztack[i]))

    def print_aliases(self):
        print('Aliases: ')
        for a, v in self.store.items():
            print('  {}: {}'.format(a, v))
    
    def error(self, message):
        # better line and column display:
        line = self.program[:self.index].count('\n') + 1
        column = self.program[:self.index].rfind('\n') - self.index

        source_start = max(0, self.index - 10)
        source_start = max(self.program.rfind('\n', source_start, self.index) + 1, source_start)
        source_end = min(len(self.program) - 1, self.index + 10)
        source_end = min(source_end, self.program.find('\n', self.index, source_end))
        source_offset = self.index - source_start

        print(self.program[source_start:source_end])
        print((' ' * source_offset) + '^')

        print('error: {} on line {}, column {}'.format(message, line, column))
    
    def execute_file(self, filename):
        try:
            with open(filename) as file:
                program = file.read()
                self.execute(program)
        except:
            print('An unexpected error occurred')
            raise
    
    def execute(self, program):
        self.program = program
        self.loop = {}
        self.index = 0

        while (self.index < len(program)):
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

            else:
                self.error('unknown symbol \'{}\''.format(rest[0]))
                break
            
            if extra_advance is None:
                extra_advance = 0

            self.index += 1 + extra_advance

if __name__ == '__main__':
    interpreter = TwoStackInterpreter()
    
    if len(sys.argv) >= 2:
        interpreter.execute_file(sys.argv[1])