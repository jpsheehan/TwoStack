'''TwoStackSourceCollection
Author: Jesse Sheehan <jesse@sheehan.nz>
'''

from twostack_source import TwoStackSource

class TwoStackSourceCollection(object):
    '''Represents the interpretation state of multiple files.'''

    def __init__(self):
        self.sources = []
        self.source_index = None
        self.source_callstack = []

    def error(self, message):
        '''Raises an interpreter error.'''
        raise NotImplementedError('TwoStackFeatureProvider.error is not implemented')

    def add_source(self, source):
        '''Adds a source to the list, switching to it if it is the first one.'''
        self.sources.append(source)

        if self.source_index is None:
            self.switch_source(len(self.sources) - 1)

        return len(self.sources) - 1

    def switch_source(self, new_index):
        '''Switches to a new source by index.'''

        self.source_callstack.append(self.source_index)
        self.source_index = new_index

    def return_source(self):
        '''Switches back to the previous source context.'''
        self.source_index = self.source_callstack.pop()

    def load_file(self, filename):
        '''Loads a new source and adds it to the list.'''
        index = None

        try:
            file = open(filename, 'r')

            src = TwoStackSource(filename, file.read())
            index = self.add_source(src)

            file.close()

        except FileNotFoundError:
            self.error('the file "{}" could not be found'.format(filename))

        except IOError:
            self.error('the file "{}" could not be read'.format(filename))

        return index

    ##### Properties #####

    @property
    def index(self):
        '''Contains the program index of the currently executing script.'''
        return self.sources[self.source_index].index

    @index.setter
    def index(self, index):
        self.sources[self.source_index].index = index

    @property
    def program(self):
        '''Contains the currently executing program.'''
        return self.sources[self.source_index].program

    @property
    def filename(self):
        '''Contains the filename of the currently executing program.'''
        return self.sources[self.source_index].filename

    @property
    def attrs(self):
        '''Contains misc attributes.'''
        return self.sources[self.source_index].attrs

    @attrs.setter
    def attrs(self, attrs):
        self.sources[self.source_index].attrs = attrs
