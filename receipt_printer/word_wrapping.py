""" Text wrapping
"""

# A lot of this is copied off of the python textwrap package
# https://github.com/python/cpython/blob/2.7/Lib/textwrap.py
# I decided against using that package so that I could
#  modify the wrapping more easily

import  string, re
from sys import stdin

# This funky little regex is just the trick for splitting
# text up into word-wrappable chunks.  E.g.
#   "Hello there -- you goof-ball, use the -b option!"
# splits into
#   Hello/ /there/ /--/ /you/ /goof-/ball,/ /use/ /the/ /-b/ /option!
# (after stripping out empty strings).
wordsep_re = re.compile(
  r'(\s+|'                                  # any whitespace
  r'[^\s\w]*\w+[^0-9\W]-(?=\w+[^0-9\W])|'   # hyphenated words
  r'(?<=[\w\!\"\'\&\.\,\?])-{2,}(?=\w))')   # em-dash

pattern_re = re.compile(wordsep_re.pattern, re.U)

def wrap(chucks, width = 32):
  """ wrap(chunks string[] [, width int]) string[]
  """

  lines = []

  # Arrange in reverse order so items can be efficiently popped
  # from a stack of chucks.
  chunks.reverse()

  while chunks:
    cur_line = [] # Current line of chunks
    cur_len = 0   # Length of the current line so far

    # First chunk on line is whitespace -- drop it, unless this
    # is the very beginning of the text (ie. no lines started yet).
    if chunks[-1].strip() == '' and lines:
      del chunks[-1]

    while chunks:
      l = len(chunks[-1])

      # Can at least squeeze this chunk onto the current line.
      if cur_len + l <= width:
        cur_line.append(chunks.pop())
        cur_len += l
      else: # Nope, this line is full
        break

    # The current line is full, and the next chunk is too big to
    # fit on *any* line (not just this one). Chop the next chunk up to fit
    if chunks and len(chunks[-1]) > width:
      longchunk = chunks[-1]
      chunks[-1] = longchunk[width:]
      chunks.append(longchunk[:width])
      # raise ValueError('Current chunk is longer than width')


    # If the last chunk on this line is all whitespace, drop it.
    if cur_line and cur_line[-1].strip() == '':
      del cur_line[-1]

    # Convert current line back to a string and store it in list
    # of all lines (return value).
    if cur_line:
      lines.append(''.join(cur_line))

  return lines


# text = "This funky little regex is just able able  able steeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeech the trick for splitting text up into word-wrappable chunks.  E.g. Hello there -- you goof-ball, use the -b option! splits into Hello/ /there/ /--/ /you/ /goof-/ball,/ /use/ /the/ /-b/ /option! (after stripping out empty strings). "
for line in stdin:

  line = line.encode('ascii','ignore')
  line = line.decode('ascii')
  chunks = pattern_re.split(line)

  output = wrap(chunks)

  print('\n'.join(output),end='')
