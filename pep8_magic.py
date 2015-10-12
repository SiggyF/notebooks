# magic function that checks a cell for pep8 compliance
# %%pep8
# a=1
# should give an error about missing spaces

import sys
import tempfile
import io
import logging

from IPython.core.magic import register_cell_magic


def load_ipython_extension(ipython):
    # The `ipython` argument is the currently active `InteractiveShell`
    # instance, which can be used in any way. This allows you to register
    # new magics or aliases, for example.
    pass


def unload_ipython_extension(ipython):
    # If you want your extension to be unloadable, put that logic here.
    pass


@register_cell_magic
def pep8(line, cell):
    """pep8 cell magic"""
    import pep8
    logger = logging.getLogger('pep8')
    logger.setLevel(logging.INFO)
    # output is written to stdout
    # remember and replace
    old_stdout = sys.stdout
    # temporary replace
    sys.stdout = io.StringIO()
    # store code in a file, todo unicode
    with tempfile.NamedTemporaryFile() as f:
        # save to file
        f.write(bytes(cell + '\n', 'UTF-8'))
        # make sure it's written
        f.flush()
        # now we can check the file by name.
        # we might be able to use 'stdin', have to check implementation
        pep8style = pep8.StyleGuide()
        # check the filename
        pep8style.check_files(paths=[f.name])
        # split lines
        stdout = sys.stdout.getvalue().splitlines()
    for line in stdout:
        logger.info(line)
    # restore
    sys.stdout = old_stdout
    return
