"""
Python program to replace the compiler

"""
from git import Repo
import os
import time

import sys

import subprocess

COMPILER_COMMAND = 'python' # replace with whatever usually used in the commandline ex. python3

def add_commit(id, push = True):
    """
    Add current changes and commit
    """
    # need to check if anything in repo has changed
    repo = Repo(os.getcwd())
    hcommit = repo.head.commit
    
    print(hcommit.diff(None)[0].score)


    repo.git.add('.')
    repo.git.commit('-m', id)
    if push:
        repo.remotes.origin.push()

if __name__ == '__main__':
    id = str(time.time())
    add_commit(id + '_start')
    
    command = [COMPILER_COMMAND] + sys.argv[1:]

    process = subprocess.run(command)
    with open('./runs.txt', 'a') as f:
        record = '{} , {} , error_code: {} \n'.format(sys.argv[1], id, process.returncode)
        f.write(record)

    add_commit(id + '_end', push=True)
    
