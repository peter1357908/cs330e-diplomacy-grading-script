modified from cs330e-collatz-grading-script:

https://github.com/peter1357908/cs330e-collatz-grading-script/

Main differences:
1. does not check for optional files (Collatz had a sphere challenge optional file)
2. checks for Git flow files like `.gitignore` and `gitlab-ci.yml`.
3. commented out some print statements
4. checks for group number (a new field added to the JSON file at the time of this project)
5. account for multiple acceptance test files
6. overall more modularization
7. hard checks the number of unit tests
8. uses `subprocess.run()` where possible (replacing the `call()`, `check_call()`, `check_output()`, and `popen()` calls)
9. added a simple progress tracker
10. silenced a lot of commands by directing output to `subprocess.DEVNULL` as well as silencing makefile commands with `@`

