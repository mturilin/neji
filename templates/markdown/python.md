## Allowed packages

Allowing arbtrarty packages in Python would pose a security threat for the server. Anybody could use for example
subprocess module to execute any code on the server. I limited packages you can import in your program to this list:

- string
- re
- struct
- datetime
- numbers
- math
- decimal
- fractions
- random
- itertools
- functool
- operator
- pickle
- cPickle
- zlib
- gzip
- bz2
- zipfile
- csv
- io
- time
- threading
- time
- json

Please contact me if you think I need to enable some other packages.

## Allowed keywords

Some keywords like "eval" and "execfile" allow the developer doing pretty much anything on the computer. Because of that
we prohibited these keywords to be a function or variable name (as a full word). However, they could be a part of the
name, like eval1. Here are some examples.

These statements are prohibited:

- eval = "bla bla"
- execfile("del_hard_drive.py")

These statements are allowed:

- eval1("bla bla")
- execfile_num1("lalala.py")