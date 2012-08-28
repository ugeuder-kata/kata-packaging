unittests can be run using nosetests or just by calling them directly
using command "python test<name>.py"

They are independent of the current working directory so you can call
them also directly from the parent directory when working on the code.

Only nosetests picks up all files containing tests. When using python
command directly you need to call the files one by one. (I did not
bother to write our own testall.py.)
