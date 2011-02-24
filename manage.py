#!/usr/bin/env python
import os, site, sys

# This code is based on: https://github.com/fwenzel/reporter
ROOT = os.path.dirname(os.path.abspath(__file__))
path = lambda *parts: os.path.join(ROOT, *parts)

# setup sys.path
prev_sys_path = list(sys.path)

site.addsitedir(path('apps'))
site.addsitedir(path('external'))

# Move the new items to the front of sys.path. (via virtualenv)
new_sys_path = []
for item in list(sys.path):
    if item not in prev_sys_path:
        new_sys_path.append(item)
        sys.path.remove(item)
sys.path[:0] = new_sys_path


from django.core.management import execute_manager, setup_environ

try:
    import settings_local as settings
except ImportError:
    try:
        import settings
    except ImportError:
        sys.stderr.write("'Required settings(_local)?.py' missing! Exiting.")
        raise

setup_environ(settings)

if __name__ == "__main__":
    __import__("blogging")
    execute_manager(settings)
