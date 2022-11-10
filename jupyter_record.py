from IPython.core.magic import Magics, magics_class, line_magic, cell_magic
#from IPython.utils.capture import capture_output

from git import Repo
import os
import time
import sys
import subprocess

#COMPILER_COMMAND = 'python' # replace with whatever usually used in the commandline ex. python3

MAX_SIZE = 20000000

def check_diff(repo):
    hcommit = repo.head.commit
    
    diffs = hcommit.diff(None)

    # for diff_added in diffs.iter_change_type('M'):
    #     print(diff_added)

    if len(diffs) == 0:
        return False
    else:
        return True

def add_commit(id, check_changed = True, push = True):
    """
    Add current changes and commit
    """
    # need to check if anything in repo has changed
    repo = Repo(os.getcwd())
    
    if check_changed:
        changed = check_diff(repo)
    else:
        changed = True    
    if changed:
        repo.git.add('.')
        repo.git.commit('-m', id)
        if push:
            repo.remotes.origin.push()
        return changed
    
    else:
        return changed

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
    def git_commit(self, line, cell):
        #()
        # print("Full access to the main IPython object:", self.shell)
        # print(type(self.shell))
        # print()
        # for key in list(self.shell.user_ns.keys()):
        #     print(key)
        #     print(self.shell.user_ns[key])
        result = self.shell.run_cell(cell)
        id = str(time.time())
        self.update_record(cell, id, result)
        #self.update_id()
        # #committed = add_commit(id + '_start', push = False)
        add_commit(id + '_end', push=True)

def load_ipython_extension(ipython):
    """
    Any module file that define a function named `load_ipython_extension`
    can be loaded via `%load_ext module.path` or be configured to be
    autoloaded by IPython at startup time.
    """
    # You can register the class itself without instantiating it.  IPython will
    # call the default constructor on it.
    ipython.register_magics(AutoCommit)