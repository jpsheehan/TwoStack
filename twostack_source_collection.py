'''TwoStackSourceCollection
Author: Jesse Sheehan <jesse@sheehan.nz>
'''

from twostack_source import TwoStackSource

class TwoStackSourceCollection(object):
    '''Represents the interpretation state of multiple files.'''

    def __init__(self):
        self.sources = []
        self.source_index = None

        self.__attrs = {}

    def error(self, message):
        '''Raises an interpreter error.'''
        raise NotImplementedError('TwoStackFeatureProvider.error is not implemented')

    def add_source(self, source):
        '''Adds a source to the list, switching to it if it is the first one.'''
        self.sources.append(source)

        if self.source_index is None:
            self.switch_source(-1)

    def switch_source(self, new_index):
        '''Switches to a new source by index.'''
        self.source_index = new_index

        if self.__attrs is not None:
            self.sources[self.source_index].attrs = self.__attrs
            self.__attrs = None

    def load_file(self, filename):
        '''Loads a new source and adds it to the list.'''

        try:
            file = open(filename, 'r')

            src = TwoStackSource()
            src.load(filename, file.read())
            self.add_source(src)

        except FileNotFoundError:
            self.error('the file "{}" could not be found'.format(filename))

        except IOError:
            self.error('the file "{}" could not be read'.format(filename))

        finally:
            file.close()

    ##### Properties #####

    @property
    def index(self):
        '''Contains the index of the currently executing script.'''
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
        if not self.source_index:
            return self.__attrs
        else:
            return self.sources[self.source_index].attrs

    @attrs.setter
    def attrs(self, attrs):
        if not self.source_index:
            self.__attrs = attrs
        else:
            self.sources[self.source_index].attrs = attrs
