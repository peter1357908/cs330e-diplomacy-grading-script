Not accounting for input from STDIN and output to STDOUT

submitting invalid JSON files:
1. submitting the schema file
2. taking away fields from the schema file (add mandatory fields to JSON files?)

Special traits of each grader acceptance test:
1. multiple (more than 2) armies contending for one cities, and multiple armies in support mode, with one army being victorious
2. multiple armies contending for one cities, and multiple armies in support mode, with no army being victorious. Also, one army tries to move into a city whose previous occupant died from the conflict.
3. multiple armies contending for one cities, and multiple armies in support mode, with one support being invalidated by an army moving into the supporting city, resulting in one army being victorious (if the support wasn't invalidated, then there would be no victor).
4. multiple armies contending for one cities, and one supporting army who became itself under attack; another army also tries to move into the city of the army attacking the supporting army.
5. multiple armies contending for one cities, and multiple armies in support mode, with no victor. One army tries to support a supporting army that was not under attack (such a support shouldn't affect the evaluation)



Typical issues of student code:
1. failed to account for support properly when multiple armies besiege one city
2. failed to properly evaluate the case where one attacking army's city is itself under attack (an attacking army does not contend for their previous location)

Either 1. and 2. above can result in an incorrect output where multiple armies occupy the same city