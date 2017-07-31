"""
The formal interpreter for uclang.

; - Discards the top item
: - Duplicates the top item
\ - Swaps the top two items
\\ - Swaps the top and third-from-top items
/
//
+
-
*
^
[ - loops until the top element of the stack is equal to 0, then jumps to the corresponding ]

"""

class UcLang(object):

  def __init__(self):
    self.reset()
  
  def reset(self):
    self.stack = []
    self.store = {}
  
  def error(self, message):
    source_start = max(0, self.index - 10)
    source_start = max(self.program.rfind('\n', source_start, self.index) + 1, source_start)
    source_end = min(len(self.program) - 1, self.index + 10)
    source_end = min(source_end, self.program.find('\n', self.index, source_end))
    source_offset = self.index - source_start

    print(self.program[source_start:source_end])
    print((' ' * source_offset) + '^')

    print('error: {} on line {}, column {}'.format(message, self.line_number, self.char_number))
  
  def execute(self, program):
    self.line_number = 1
    self.char_number = 1
    self.program = program
    self.loop = {}

    self.index = 0

    while (self.index < len(program)):
      p = program[self.index:]
      extra_advance = 0

      if p[0] == ' ':
        pass
      elif p[0] == '\n':
        self.line_number += 1
        self.char_number = 0
      elif p[0] == ';': # discard
        if len(self.stack) > 0:
          self.stack.pop()
        else:
          self.error('not enough items on stack')
          break
      elif p[0] == ':': # duplicate
        if len(self.stack) > 0:
          self.stack.append(self.stack[-1])
        else:
          self.error('not enough items on stack')
          break
      elif p[0] == '\\':
        if len(self.stack) > 1:
          if len(p) > 1 and p[1] == '\\': # rotate
            if len(self.stack) > 2:
              s = self.stack.pop()
              t = self.stack.pop()
              u = self.stack.pop()
              self.stack.append(s)
              self.stack.append(t)
              self.stack.append(u)
              extra_advance = 1
            else:
              self.error('not enough items on stack')
              break
          else: # swap
            s = self.stack.pop()
            t = self.stack.pop()
            self.stack.append(s)
            self.stack.append(t)
        else:
          self.error('not enough items on stack')
          break
      elif p[0] == '+': # add
        if len(self.stack) > 1:
          self.stack.append(self.stack.pop() + self.stack.pop())
        else:
          self.error('not enough items on stack')
          break
      elif p[0] == '-': # subtract
        if len(self.stack) > 1:
          self.stack.append(self.stack.pop() - self.stack.pop())
        else:
          self.error('not enough items on stack')
          break
      elif p[0] == '*': # multiply
        if len(self.stack) > 1:
          self.stack.append(self.stack.pop() * self.stack.pop())
        else:
          self.error('not enough items on stack')
          break
      elif p[0] == '/':
        if len(p) > 1 and p[1] == '/': # integer division
          if len(self.stack) > 1:
            self.stack.append(self.stack.pop() // self.stack.pop())
            extra_advance = 1
          else:
            self.error('not enough items on stack')
        else:
          if len(self.stack) > 1: # division
            self.stack.append(self.stack.pop() / self.stack.pop())
          else:
            self.error('not enough items on stack')
            break
      elif p[0] == '%': # modulus
        if len(self.stack) > 1:
          self.stack.append(self.stack.pop() % self.stack.pop())
        else:
          self.error('not enough items on stack')
          break
      elif p[0] == '^': # power
        if len(self.stack) > 1:
          self.stack.append(self.stack.pop() ** self.stack.pop())
        else:
          self.error('not enough items on stack')
          break
        
      elif p[0] == '[':
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

        if len(self.stack) > 0:
          if self.stack[-1] == 0:
            self.index = self.loop[self.index]
        else:
          self.error('not enough items on stack')
          break
      elif p[0] == ']':
        self.index = self.loop[self.index] - 1
      elif p[0].isdigit():
        d = 1
        while d < len(p) and p[d].isdigit():
          d += 1
        self.stack.append(int(p[:d]))
        extra_advance = d - 1
      elif p[0] == '#':
        d = 1
        while d < len(p) and p[d] != '\n':
          d += 1
        extra_advance += d
      elif p[0] == '_':
        print('Debug Information:')
        print('Stack: ')
        for i in range(len(self.stack)):
          print('  {}: {}'.format(i, self.stack[i]))
        valid = ['c', 'q']
        prompt = '(c, q) > '
        c = input(prompt)
        while c not in valid:
          c = input(prompt)
        if c == 'c':
          pass
        elif c == 'q':
          break
        else:
          self.error('unknown command')
      else:
        self.error('unknown symbol \'{}\''.format(p[0]))
        break

      self.char_number += 1 + extra_advance
      self.index += 1 + extra_advance

    for i in range(len(self.stack)):
      print('{}: {}'.format(i, self.stack[i]))

with open('program.u') as file:
  l = UcLang()
  program = file.read()
  l.execute(program)