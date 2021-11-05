from IPython.core.magic import Magics, magics_class, line_magic, cell_magic
#from IPython.utils.capture import capture_output

from git import Repo
import os
import time
import sys
import subprocess

COMPILER_COMMAND = 'python' # replace with whatever usually used in the commandline ex. python3

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

    @cell_magic
    def git_commit(self, line, cell):
        #with capture_output(True, False, True) as io:
        self.shell.run_cell(cell)
        id = str(time.time())
        #committed = add_commit(id + '_start', push = False)
        add_commit(id + '_end', check_changed = True, push=True)
        # Make a beep here somehow ?
        #io.show()

def load_ipython_extension(ipython):
    """
    Any module file that define a function named `load_ipython_extension`
    can be loaded via `%load_ext module.path` or be configured to be
    autoloaded by IPython at startup time.
    """
    # You can register the class itself without instantiating it.  IPython will
    # call the default constructor on it.
    ipython.register_magics(AutoCommit)