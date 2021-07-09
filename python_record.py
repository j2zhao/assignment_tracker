"""
Python program to replace the compiler

"""
from git import Repo
import os
import time

import sys

import subprocess

COMPILER_COMMAND = 'python' # replace with whatever usually used in the commandline ex. python3

def add_commit(id):
    """
    Add current changes and commit
    """
    repo = Repo(os.getcwd())
    repo.git.add('.')
    repo.git.commit('-m', id)

if __name__ == '__main__':
    id = str(time.time())
    add_commit(id + '_start')
    
    command = [COMPILER_COMMAND] + sys.argv[1:]

    process = subprocess.run(command)
    with open('./runs.txt', 'a') as f:
        f.write(id + ', error_code: ' + str(process.returncode))

    add_commit(id + '_end')
    
