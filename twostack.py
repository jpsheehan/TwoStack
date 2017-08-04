import sys

"""
The formal interpreter for TwoStack.
"""

class TwoStackInterpreter(object):

  def __init__(self):
    self.reset()

    self.commands = {
      '?': {
        'name': 'cond jump',
        'min': 2,
        'function': self.op_condjump
      },
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
      '|': {
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
      '//': {
        'name': 'int divide',
        'min': 2,
        'function': self.op_intdivide
      },
      '%': {
        'name': 'modulo',
        'min': 2,
        'function': self.op_modulo
      },
      '^': {
        'name': 'power',
        'min': 2,
        'function': self.op_power
      },
      '.': {
        'name': 'print',
        'min': 1,
        'function': self.op_print
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
      '#': {
        'name': 'comment',
        'min': 0,
        'function': self.op_comment
      },
      '_': {
        'name': 'debug',
        'min': 0,
        'function': self.op_debug
      },
      '@': {
        'name': 'exec block',
        'min': 0,
        'function': self.op_execblock
      },
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
      ',': {
        'name': 'read char',
        'min': 0,
        'function': self.op_readchar
      },
      '&': {
        'name': 'logical and',
        'min': 2,
        'function': self.op_logicaland
      }
    }
  
  def op_logicaland(self, p):
    ''''''
    a = self.stack.pop()
    b = self.stack.pop()
    self.stack.append(int(a and b))
  
  def op_condjump(self, p):
    ''''''
    if self.stack.pop():
      self.op_execblock(p)

  def op_readchar(self, p):
    '''Reads a character from stdin or -1 if empty.'''
    if len(self.input) > 0:
      self.stack.append(ord(self.input[0]))
      self.input = self.input[1:]
    else:
      self.input = input('> ')
      
      if len(self.input) > 0:
        self.op_readchar(p)
      else:
        self.stack.append(-1)

  def op_condgreaterthan(self, p):
    ''''''
    a = self.stack.pop()
    self.stack.append(int(self.stack.pop() > a))
  
  def op_condlessthan(self, p):
    ''''''
    a = self.stack.pop()
    self.stack.append(int(self.stack.pop() < a))

  def op_condequal(self, p):
    ''''''
    self.stack.append(int(self.stack.pop() == self.stack.pop()))
  
  def op_not(self, p):
    ''''''
    self.stack.append(int(not self.stack.pop()))
  
  def op_execblock(self, p):
    ''''''
    self.callstack.append(self.index)
    self.index = self.stack.pop()
  
  def op_blockbegin(self, p):
    ''''''
    depth = 1
    offset = 1
    while offset < len(p) and depth > 0:
      if p[offset] == '}':
        depth -= 1
      elif p[offset] == '{':
        depth += 1
      offset += 1

    self.stack.append(self.index)

    return offset - 1
  
  def op_blockend(self, p):
    ''''''
    self.index = self.callstack.pop()
  
  def op_aliasrecall(self, p):
    ''''''
    d = 0
    while d < len(p) and p[d].isalpha():
      d += 1
    if d == 0:
      self.error('alias cannot be empty')
      return d
    alias = p[0:d]

    if alias in self.store.keys():
      self.stack.append(self.store[alias])
    else:
      self.error('alias does not exist')

    return d - 1

  def op_aliasdef(self, p):
    ''''''
    d = 1
    while d < len(p) and p[d].isalpha():
      d += 1
    if d == 1:
      self.error('alias definition cannot be empty')
      return d
    alias = p[1:d]
    value = self.stack.pop()
    self.store[alias] = value
    return d - 1

  def op_stringliteral(self, p):
    ''''''
    d = 1
    while d < len(p) and p[d] != '"':
      self.stack.append(ord(p[d]))
      d += 1
    return d
  
  def op_intliteral(self, p):
    ''''''
    d = 1
    while d < len(p) and p[d].isdigit():
      d += 1
    self.stack.append(int(p[:d]))
    return d - 1
  
  def op_comment(self, p):
    d = 1
    while d < len(p) and p[d] != '\n':
      d += 1
    self.op_newline(p)
    return d

  def op_newline(self, p):
    ''''''
    self.line_number += 1
    self.char_number = 0

  def op_whitespace(self, p):
    ''''''
    pass
  
  def op_loopbegin(self, p):
    ''''''
    if self.index not in self.loop.keys():
      depth = 1
      offset = 1
      while offset < len(p) and depth > 0:
        if p[offset] == ']':
          depth -= 1
        elif p[offset] == '[':
          depth += 1
        else:
          offset += 1

      self.loop[self.index] = self.index + offset
      self.loop[offset + self.index] = self.index

    if len(self.stack) == 0 or self.stack[-1] == 0:
      self.index = self.loop[self.index]
  
  def op_loopend(self, p):
    ''''''
    self.index = self.loop[self.index] - 1

  def op_debug(self, p):
    ''''''
    self.debug()
  
  def op_stackswap(self, p):
    ''''''
    t = self.stack
    self.stack = self.ztack
    self.ztack = t

  def op_crosspop(self, p):
    ''''''
    self.ztack.append(self.stack.pop())

  def op_print(self, p):
    ''''''
    print(chr(self.stack[-1]), end='')
    sys.stdout.flush()

  def op_discard(self, p):
    '''Pop the topmost item of the stack.'''
    self.stack.pop()
  
  def op_duplicate(self, p):
    '''Push a copy of the topmost item of the stack.'''
    self.stack.append(self.stack[-1])
  
  def op_swap(self, p):
    '''Swap the topmost two elements of the stack.'''
    if len(p) > 1 and p[1] == '\\':
      if len(self.stack) > 2:
        self.op_3swap(p)
        return 1
      else:
        self.error('not enough items on stack')
    else:
      s = self.stack.pop()
      t = self.stack.pop()
      self.stack.append(s)
      self.stack.append(t)
  
  def op_3swap(self, p):
    '''Swap the topmost and third-topmost elements of the stack.'''
    s = self.stack.pop()
    t = self.stack.pop()
    u = self.stack.pop()
    self.stack.append(s)
    self.stack.append(t)
    self.stack.append(u)
  
  def op_add(self, p):
    '''Pop the two topmost elements and add them, pushing the result.'''
    self.stack.append(self.stack.pop() + self.stack.pop())
  
  def op_subtract(self, p):
    ''''''
    a = self.stack.pop()
    self.stack.append(self.stack.pop() - a)
  
  def op_multiply(self, p):
    ''''''
    self.stack.append(self.stack.pop() * self.stack.pop())
  
  def op_divide(self, p):
    ''''''
    if len(p) > 1 and p[1] == '/': # integer division
      if len(self.stack) > 1:
        self.op_intdivide(p)
        return 1
      else:
        self.error('not enough items on stack')
    else:
      if len(self.stack) > 1: # division
        a = self.stack.pop()
        self.stack.append(self.stack.pop() / a)
      else:
        self.error('not enough items on stack')
  
  def op_intdivide(self, p):
    ''''''
    a = self.stack.pop()
    self.stack.append(self.stack.pop() // a)

  def op_modulo(self, p):
    ''''''
    a = self.stack.pop()
    self.stack.append(self.stack.pop() % a)
  
  def op_power(self, p):
    ''''''
    self.stack.append(self.stack.pop() ** self.stack.pop())
  
  def reset(self):
    self.stack = []
    self.ztack = []
    self.store = {}
    self.callstack = []
    self.input = ''
  
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
    self.line_number = 1
    self.char_number = 1
    self.program = program
    self.loop = {}

    self.index = 0
    while (self.index < len(program)):
      p = program[self.index:]
      extra_advance = None

      if p[0] in self.commands.keys():
        cmd = self.commands[p[0]]
        if len(self.stack) >= cmd['min']:
          extra_advance = self.commands[p[0]]['function'](p)
        else:
          self.error('not enough elements on the stack')
          break
      elif p[0].isdigit():
        # shim to get integer literals working
        extra_advance = self.op_intliteral(p)
      elif p[0].isalpha():
        # shim to get alias recollection without any leading symbols
        extra_advance = self.op_aliasrecall(p)
      else:
        self.error('unknown symbol \'{}\''.format(p[0]))
        break
      
      if extra_advance is None:
        extra_advance = 0

      self.char_number += 1 + extra_advance
      self.index += 1 + extra_advance

if __name__ == '__main__':
  interpreter = TwoStackInterpreter()
  
  if len(sys.argv) >= 2:
    interpreter.execute_file(sys.argv[1])
    #interpreter.print_stack()