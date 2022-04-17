How to run:

0. go to the same folder as the `makefile`
1. download the group JSON submissions from Canvas and save them in `group_JSON_submissions`
2. download the evaluation JSON submissions from Canvas and save them in `evaluation_JSON_submissions`
3. in the same directory, run `make`
4. you can simply `make` again after any update to the submissions files

modified from cs330e-collatz-grading-script:

https://github.com/peter1357908/cs330e-collatz-grading-script/

Main differences (updates):
1. no longer checks for optional files (Collatz had a sphere challenge optional file)
2. checks for Git flow files like `.gitignore` and `.gitlab-ci.yml`.
3. commented out some print statements
4. checks for group number (a new field added to the JSON file at the time of this project)
5. account for multiple acceptance test files
6. overall more modularization (easier to adapt to different projects)
7. hard-checks the number of unit tests (3 for this project)
8. uses `subprocess.run()` where possible (replacing the `call()`, `check_call()`, `check_output()`, and `popen()` calls)
9. added a simple progress tracker
10. silenced a lot of commands by directing output to `subprocess.DEVNULL` as well as silencing makefile commands with `@`

