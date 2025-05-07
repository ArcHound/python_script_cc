# python_script_cc

A personal cookiecutter template for simple python3 scripts.

To use simply run `cookiecutter gh:ArcHound/python_script_cc`. 

## Features

 - load env vars from `.env` file (these might be used in place of cli options!),
 - accept `stdin` via pipe or use a file specified in an option (if you'd like),
 - post gen hook to create virtual environment using `uv` (must be [installed](https://docs.astral.sh/uv/getting-started/installation/) beforehand!),
 - return to `stdout` or to a file,
 - option for logging verbosity level,
 - built-in profiling support,
 - decorator for measuring time elapsed (log with informative severity),
 - option for including the `requests` lib and `requests_cache` lib,
    - few options for a default service - name, url and bearer token,
    - proxy options for requests session,
 - python gitignore from [https://github.com/github/gitignore/blob/main/Python.gitignore](https://github.com/github/gitignore/blob/main/Python.gitignore).
