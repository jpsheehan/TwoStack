'''TwoStackFeatureProvider
Author: Jesse Sheehan <jesse@sheehan.nz>

Contains the TwoStackFeatureProvider which defines most of the operators in the language.
'''

import sys
import os

from twostack_source import TwoStackSource

class TwoStackFeatureProvider(TwoStackSource):
    '''Implements the core language functionailty.'''

    def __init__(self):
        super().__init__()
        self.stack = []
        self.ztack = []
        self.store = {}
        self.callstack = []

        # the command manifest contains some basic data about each operator
        # such as the minimum number of elements on the stack, etc
        self.commands = {

            # ===== Mathematical Operators ===== #
            '+': {
                'name': 'add',
                'min': 2,
                'function': self.op_add
            },
            '-': {
                'name': 'subtract',
                'min': 2,
                'function': self.op_subtract
            },
            '*': {
                'name': 'multiply',
                'min': 2,
                'function': self.op_multiply
            },
            '/': {
                'name': 'divide',
                'min': 2,
                'function': self.op_divide
            },
            '%': {
                'name': 'modulo',
                'min': 2,
                'function': self.op_modulo
            },
            '**': {
                'name': 'power',
                'min': 2,
                'function': self.op_power
            },

            # ===== Stack Operators ===== #
            ';': {
                'name': 'discard',
                'min': 1,
                'function': self.op_discard
            },
            ':': {
                'name': 'duplicate',
                'min': 1,
                'function': self.op_duplicate
            },
            '\\': {
                'name': 'swap',
                'min': 2,
                'function': self.op_swap
            },
            '\\\\': {
                'name': '3-swap',
                'min': 3,
                'function': self.op_3swap
            },
            '`': {
                'name': 'crosspop',
                'min': 1,
                'function': self.op_crosspop
            },
            '$': {
                'name': 'stackswap',
                'min': 0,
                'function': self.op_stackswap
            },

            # ===== Boolean/Conditional Operators ===== #
            '!': {
                'name': 'not',
                'min': 1,
                'function': self.op_not
            },
            '=': {
                'name': 'equal to',
                'min': 2,
                'function': self.op_condequal
            },
            '<': {
                'name': 'less than',
                'min': 2,
                'function': self.op_condlessthan
            },
            '>': {
                'name': 'greater than',
                'min': 2,
                'function': self.op_condgreaterthan
            },
            '&': {
                'name': 'logical and',
                'min': 2,
                'function': self.op_logicaland
            },
            '|': {
                'name': 'logical or',
                'min': 2,
                'function': self.op_logicalor
            },
            '^': {
                'name': 'logical xor',
                'min': 2,
                'function': self.op_logicalxor
            },

            # ===== Code Execution ===== #

            '?': {
                'name': 'cond jump',
                'min': 2,
                'function': self.op_condjump
            },
            '@': {
                'name': 'exec block',
                'min': 0,
                'function': self.op_execblock
            },

            # ===== Blocks ===== #
            '{': {
                'name': 'block begin',
                'min': 0,
                'function': self.op_blockbegin
            },
            '}': {
                'name': 'block end',
                'min': 0,
                'function': self.op_blockend
            },
            '[': {
                'name': 'loop begin',
                'min': 0,
                'function': self.op_loopbegin
            },
            ']': {
                'name': 'loop end',
                'min': 0,
                'function': self.op_loopend
            },

            # ===== Input/Output ===== #
            '.': {
                'name': 'output',
                'min': 1,
                'function': self.op_output
            },
            ',': {
                'name': 'input',
                'min': 0,
                'function': self.op_input
            },

            # ===== Miscellaneous ===== #
            '~': {
                'name': 'alias def',
                'min': 1,
                'function': self.op_aliasdef
            },
            '"': {
                'name': 'string literal',
                'min': 0,
                'function': self.op_stringliteral
            },
            '\n': {
                'name': 'newline',
                'min': 0,
                'function': self.op_newline
            },
            ' ': {
                'name': 'whitespace',
                'min': 0,
                'function': self.op_whitespace
            },
            '^[a-zA-Z]+': {
                'name': 'alias recall',
                'min': 0,
                'function': self.op_aliasrecall,
                'is_regex': True
            },
            '^[0-9]+': {
                'name': 'integer literal',
                'min': 0,
                'function': self.op_intliteral,
                'is_regex': True
            }
        }

    # ===== Mathematical Operators ===== #
    def op_add(self):
        '''The add operator.
        Pop the two topmost elements and add them.
        Pushing the result.
        '''
        elem1 = self.stack.pop()
        elem2 = self.stack.pop()
        self.stack.append(elem1 + elem2)

    def op_subtract(self):
        '''The subtract operator.
        Pop two elements and subtract the first from the second.
        Push the result.
        '''
        elem1 = self.stack.pop()
        elem2 = self.stack.pop()
        self.stack.append(elem2 - elem1)

    def op_multiply(self):
        '''The multiply operator.
        Pop two elements and multiply them.
        Push the result.
        '''
        elem1 = self.stack.pop()
        elem2 = self.stack.pop()
        self.stack.append(elem1 * elem2)

    def op_divide(self):
        '''The division operator.
        Pops two elements and divides the second by the first.
        Pushes the quotient.
        '''
        elem1 = self.stack.pop()
        elem2 = self.stack.pop()
        self.stack.append(elem2 // elem1)

    def op_modulo(self):
        '''The modulus operator.
        Pops two elements and divides the second by the first.
        Pushes the remainder.
        '''
        elem1 = self.stack.pop()
        elem2 = self.stack.pop()
        self.stack.append(elem2 % elem1)

    def op_power(self):
        '''The power operator.
        Pops two elements and the second to the first power.
        Pushes the result.
        '''
        elem1 = self.stack.pop()
        elem2 = self.stack.pop()
        self.stack.append(elem2 ** elem1)

    # ===== Stack Operators ===== #
    def op_discard(self):
        '''The discard operator.
        Pop the top element from the stack.
        '''
        self.stack.pop()

    def op_duplicate(self):
        '''The duplicate operator.
        Push a copy of the top element of the stack.
        '''
        self.stack.append(self.stack[-1])

    def op_swap(self):
        '''The swap operator.
        Swap the top two elements from the stack.
        '''
        elem1 = self.stack.pop()
        elem2 = self.stack.pop()
        self.stack.append(elem1)
        self.stack.append(elem2)

    def op_3swap(self):
        '''The 3Swap operator.
        Swap the topmost and third-topmost elements from the stack.
        '''
        elem1 = self.stack.pop()
        elem2 = self.stack.pop()
        elem3 = self.stack.pop()
        self.stack.append(elem1)
        self.stack.append(elem2)
        self.stack.append(elem3)
        return 1

    def op_stackswap(self):
        '''The stackswap operator.
        Swap the main stacks so that stack now references ztack and ztack now references stack.
        '''
        temp_stack = self.stack
        self.stack = self.ztack
        self.ztack = temp_stack

    def op_crosspop(self):
        '''The crosspop operator.
        Pop the top element from the stack and push it to the ztack.
        '''
        elem = self.stack.pop()
        self.ztack.append(elem)

    # ===== Boolean/Conditional Operators ===== #

    def op_not(self):
        '''The unary not operator.
        Pop the top element and push the boolean not as an integer.
        '''
        elem = self.stack.pop()
        self.stack.append(int(not elem))

    def op_condequal(self):
        '''The equal condition.
        Pop the top two elements and check whether the first element is equal to the first.
        Push the boolean integer result.
        '''
        elem1 = self.stack.pop()
        elem2 = self.stack.pop()
        self.stack.append(int(elem1 == elem2))

    def op_condlessthan(self):
        '''The less than condition.
        Pop the top two elements and check whether the second element is less than the first.
        Push the boolean integer result.
        '''
        elem1 = self.stack.pop()
        elem2 = self.stack.pop()
        self.stack.append(int(elem2 < elem1))

    def op_condgreaterthan(self):
        '''The greater than operator.
        Pop the top two elements and check whether the second element is greater than the first.
        Push the boolean integer result.
        '''
        elem1 = self.stack.pop()
        elem2 = self.stack.pop()
        self.stack.append(int(elem2 > elem1))

    def op_logicaland(self):
        '''The logical 'and' operator.
        Pops the top two elements and pushes the boolean result.
        '''
        elem1 = self.stack.pop()
        elem2 = self.stack.pop()
        self.stack.append(int(elem1 and elem2))

    def op_logicalor(self):
        '''The logical 'or' operator.
        Pops the top two elements and pushes the boolean result.
        '''
        elem1 = self.stack.pop()
        elem2 = self.stack.pop()
        self.stack.append(int(elem1 or elem2))

    def op_logicalxor(self):
        '''The logical 'xor' operator.
        Pops the top two elements and pushes the boolean result.
        '''
        elem1 = self.stack.pop()
        elem2 = self.stack.pop()
        self.stack.append(int(elem1 ^ elem2))

    # ===== Code Execution ===== #

    def op_condjump(self):
        '''The conditional jump operator.
        If the top element of the stack is not 0, pop the next element and use that as the index.
        '''
        if self.stack.pop():
            self.op_execblock()

    def op_execblock(self):
        '''Jump to an arbitrary location.
        Store the current location on the callstack.
        Pop the top element from the stack and use that as the index.
        '''
        self.callstack.append(self.index)
        self.index = self.stack.pop()

    # ===== Blocks ===== #

    def op_blockbegin(self):
        '''Signal the beginning of a code block.
        Push the index to the stack.
        Advance the index to the end of the block.
        '''
        # find the index of the matching }
        rest = self.program[self.index:]
        depth = 1
        offset = 1
        while offset < len(rest) and depth > 0:
            if rest[offset] == '}':
                depth -= 1
            elif rest[offset] == '{':
                depth += 1
            offset += 1

        self.stack.append(self.index)

        return offset - 1

    def op_blockend(self):
        '''Signals the end of a code block.
        Return to where the index was before the block was run.
        '''
        self.index = self.callstack.pop()

    def op_loopbegin(self):
        '''Signals the beginning of a loop.
        Checks if the loop is cached in self.loop, if not, find the matching ] and cache it.
        Peek the stack and checks if the value is equal to 0, if so,
        jump to the matching ], otherwise continue the loop.
        '''

        # check if the loop does not exist in the cache
        if self.index not in self.loop.keys():
            rest = self.program[self.index:]

            depth = 1
            offset = 1
            while offset < len(rest) and depth > 0:

                if rest[offset] == ']':
                    depth -= 1

                elif rest[offset] == '[':
                    depth += 1

                offset += 1

            offset -= 1

            # set cache entries for the start and end of the loop
            self.loop[self.index] = self.index + offset
            self.loop[offset + self.index] = self.index

        # check the loop condition
        if not self.stack or (self.stack and self.stack[-1] == 0):
            self.index = self.loop[self.index]

    def op_loopend(self):
        '''Signals the end of the loop.
        Jump to the matching [ stored in the cache.
        '''
        self.index = self.loop[self.index] - 1

    # ===== Input/Output ===== #

    def op_input(self):
        '''The input operator.
        Pushes the ordinal value of the next character in the stream or -1 if the stream is empty.
        '''
        try:
            char = sys.stdin.read(1)

        except KeyboardInterrupt:
            char = ''

        if char:
            self.stack.append(ord(char))
        else:
            self.stack.append(-1)

    def op_output(self):
        '''The output operator.
        Prints the top element of the stack as an ascii character.
        This is peeked, not popped.
        '''
        try:
            char = chr(self.stack[-1])

        except ValueError:
            # handle out of range character values
            char = ''

        sys.stdout.write(char)

        # flush if char is a newline character
        if char in os.linesep:
            sys.stdout.flush()

    # ===== Miscellaneous ===== #

    def op_aliasrecall(self):
        '''Attempt to recall an alias.
        Push the alias value to the stack.
        If the alias does not exist, throw an error.
        '''
        rest = self.program[self.index:]

        # find the full alias name
        last_char_index = 0
        while last_char_index < len(rest) and rest[last_char_index].isalpha():
            last_char_index += 1

        if last_char_index == 0:
            self.error('alias cannot be empty')
            return last_char_index

        alias = rest[0:last_char_index]

        # recall the alias name if possible
        if alias in self.store.keys():
            self.stack.append(self.store[alias])
        else:
            self.error('alias does not exist')

        return last_char_index - 1

    def op_aliasdef(self):
        '''Alias definition operator.
        An alias represents an integer that can be recalled later.
        Pops the top element of the stack and assigns it to the alias.
        '''
        rest = self.program[self.index:]

        last_char_index = 1
        while last_char_index < len(rest) and rest[last_char_index].isalpha():
            last_char_index += 1

        if last_char_index == 1:
            self.error('alias definition cannot be empty')
            return last_char_index

        alias = rest[1:last_char_index]
        value = self.stack.pop()

        self.store[alias] = value

        return last_char_index - 1

    def op_stringliteral(self):
        '''Pushes a string to the stack character by character.
        If the string "hello" is pushed to the stack,
        the top element of the stack will be the integer representation of "o".
        '''
        rest = self.program[self.index:]

        string_length = 1
        while string_length < len(rest) and rest[string_length] != '"':
            char_value = ord(rest[string_length])
            self.stack.append(char_value)

            string_length += 1

        return string_length

    def op_intliteral(self):
        '''Pushes an integer literal to the stack.'''
        rest = self.program[self.index:]

        string_length = 1
        while string_length < len(rest) and rest[string_length].isdigit():
            string_length += 1

        int_value = int(rest[:string_length])
        self.stack.append(int_value)

        return string_length - 1

    def op_newline(self):
        '''A stub for newline handling.'''
        pass

    def op_whitespace(self):
        '''A stub for space handling.'''
        pass
    