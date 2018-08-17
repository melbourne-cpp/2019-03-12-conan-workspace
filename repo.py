#!/usr/bin/env python3
import os
import subprocess
import sys

SUBMODULE_PATHS = ['lmlib', 'lmeditor', 'lmengine']


def git_action(repo_dir):
    repo_toplevel_path = subprocess.check_output(
        'git rev-parse --show-toplevel'.split(' '), cwd=repo_dir)
    print(os.path.basename(repo_toplevel_path).decode('UTF-8').strip())
    subprocess.check_call(['git'] + sys.argv[1:], cwd=repo_dir)
    print('')


if __name__ == '__main__':
    assert sys.argv[1] != 'rebase', (
        'Rebasing is not safe for combined submodules and parent to avoid ' 
        'invalid refs to recorded commits that will be changed by the rebase.'
    )
    for dir_ in SUBMODULE_PATHS + ['.']:
        git_action(dir_)
