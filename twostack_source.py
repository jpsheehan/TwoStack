'''TwoStackFile
Author: Jesse Sheehan <jesse@sheehan.nz>
'''

class TwoStackSource(object):
    '''Represents the interpretation state of a single file.'''

    def __init__(self, filename, program):
        '''Load the program from a file.'''
        self.filename = filename
        self.program = program
        self.attrs = {'loops': {}, 'aliases': {}, 'callstack': []}
        self.index = 0
