Easy Change:
- Use f-strings more consistently (currently has some string concatenantions and f-strings)
- Add comments to abnormal evaluations
- check for empty JSON files
- Check unit test results (of how the tests are run on OUR end; all dots no F's)
- Record EID and send emails to EID addresses as well (just in case)
- account for missing fields in the JSON (some students who worked alone took out member 2 fields since they are not `required` in the schema)
- count unit tests better (some student don't follow the naming convention taught in the class and their tests won't be detected by the script)
- checks for JSON filename (required to have correct GitLab ID in the name)

Challenging Change:
- Make the code more efficient (run tests in parallel and keep files open instead of repeatedly opening and closing them)
- Send emails automatically
- check if each major function has documentation (try using pydoc somehow?)
