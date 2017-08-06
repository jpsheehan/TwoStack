'''TwoStackFile
Author: Jesse Sheehan <jesse@sheehan.nz>
'''

class TwoStackExecutionContext(object):
    '''Represents the current state of execution.'''

    def __init__(self, filename, program):
        '''Load the program from a file.'''
        self.filename = filename
        self.program = program
        self.index = 0

        # there is some private state
        self.attrs = {
            'loops': {},
            'aliases': {},
            'callstack': []
        }
