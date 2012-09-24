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