#!/usr/bin/env python3.6

import os
import shutil
import sys


def run():
    from django.core.management import execute_from_command_line
    
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings_dev'
    args = sys.argv[:]
    if len(args) == 2 and sys.argv[1] == 'runserver':
        # Default to serving externally if not told otherwise
        args = sys.argv + ['0.0.0.0:8080']

    execute_from_command_line(args)


if __name__ == '__main__':
    run()
