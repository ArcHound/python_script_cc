# python_script_cc
A personal cookiecutter template for simple python3 scripts.

To use simply run `cookiecutter gh:ArcHound/python_script_cc`. I recommend running `bash init.sh` to setup the virtualenv.

## Features

 - load env vars from `.env` file,
 - accept `stdin` via pipe or use a file specified in an option (if you'd like),
 - return to `stdout` or to a file,
 - option for logging verbosity level,
 - option for including the `requests` lib and `requests_cache` lib
 - python gitignore from [https://github.com/github/gitignore/blob/main/Python.gitignore](https://github.com/github/gitignore/blob/main/Python.gitignore).
