from IPython.core.magic import Magics, magics_class, line_magic, cell_magic

from git import Repo
import os
import time
import sys
import subprocess

MAX_SIZE = 20000000


@magics_class
class AutoCommit(Magics):
    index = None

    def update_record(self, cell, id, result):
        file_dire = self.update_index()
        with open(file_dire, 'a') as f:
            f.write('new run: {} \n'.format(id,))
            f.write('format error: {} \n'.format(result.error_before_exec))
            f.write('execution error: {} \n'.format(result.error_in_exec))
            f.write(cell)
    
    def update_index(self, dire = './code_history'):
        if self.index == None:
            index_dire = os.path.join(dire, 'current_index.txt')
            with open(index_dire, 'r') as f:
                self.index = int(f.readline())
        else:
            file_dire = os.path.join(dire, 'runs_{}.txt'.format(self.index))
            fsize = os.path.getsize(file_dire)
            if fsize >= MAX_SIZE:
                self.index += 1
                index_dire = os.path.join(dire, 'current_index.txt')
                with open(index_dire, 'w') as f:
                    f.write(str(self.index))

        file_dire = os.path.join(dire, 'runs_{}.txt'.format(self.index))
        return file_dire

    @cell_magic
    def log_run(self, line, cell):
        result = self.shell.run_cell(cell)
        id = str(time.time())
        self.update_record(cell, id, result)

def load_ipython_extension(ipython):
    """
    Any module file that define a function named `load_ipython_extension`
    can be loaded via `%load_ext module.path` or be configured to be
    autoloaded by IPython at startup time.
    """
    ipython.register_magics(AutoCommit)