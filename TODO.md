Easy Change:
- Use f-strings more consistently (currently has some string concatenantions and f-strings)
- Add comments to abnormal evaluations
- check for empty JSON files
- Check unit test results (of how the tests are run on OUR end; all dots no F's)
- Record EID and send emails to EID addresses as well (just in case)
- account for missing fields in the JSON (some students who worked alone took out member 2 fields since they are not `required` in the schema)

Challenging Change:
- Make the code more efficient (run tests in parallel and keep files open instead of repeatedly opening and closing them)
- Send emails automatically
