'''TwoStackFile
Author: Jesse Sheehan <jesse@sheehan.nz>
'''

class TwoStackSource(object):
    '''Represents the interpretation state of multiple files.'''

    def __init__(self):
        self.filename = ''
        self.program = ''
        self.loop = {}
        self.index = 0

    def error(self, message):
        '''Raises an interpreter error.'''
        raise NotImplementedError('TwoStackFeatureProvider.error is not implemented')

    def load_file(self, filename):
        '''Load the program from a file.'''

        try:
            file = open(filename, 'r')

            self.filename = filename
            self.program = file.read()
            self.index = 0
            self.loop = {}

        except FileNotFoundError:
            self.error('the file "{}" could not be found'.format(filename))

        except IOError:
            self.error('the file "{}" could not be read'.format(filename))

        finally:
            file.close()
