import os
import glob
import json
import subprocess
import time

# must be absolute path; assuming running in Git Bash on Windows
# make sure to run after `make clean`
base_path = 'D:/Libraries Type-D/Documents/SCHOOL/UT Austin/Spring 2022/CS 330E Elements of Software Engineering (TA)/Projects/cs330e-diplomacy-grading-script'
output_path = base_path + '/output'
num_acceptance_tests = 5
min_num_unit_tests = 3
project_basename = 'Diplomacy'
run_py_file = f'Run{project_basename}.py'
test_py_file = f'Test{project_basename}.py'
test_out_file = f'Test{project_basename}.out'
required_files = ['.gitignore', '.gitlab-ci.yml', 'makefile', 'requirements.txt', f'{project_basename}.py', run_py_file, test_py_file, test_out_file, f'{project_basename}.html', f'{project_basename}.log']

def chdir(new_dir):
	try:
		os.chdir(new_dir)
		# print(f'cd to {os.getcwd()}')
	except Exception as e:
		print(f'cd to {new_dir} failed. Exception message:\n{e}')

# first, cd to the base_path and make all the directories needed; assuming that
# `submissions` directory is in the root of the base_path, and that `repos` and `output`
# do not exist.
chdir(base_path)
os.makedirs('repos')
os.makedirs('output')

acceptance_test_filenames = []
acceptance_test_inputs = [] # each item in the list is a string of the file content
acceptance_test_outputs = [] # each item in the list is a string of the file content
for i in range(1, num_acceptance_tests + 1):
	acceptance_test_filenames.append(f'Run{project_basename}{i}.in')
	acceptance_test_filenames.append(f'Run{project_basename}{i}.out')
	# load our input and output into strings for efficiency
	with open(f'Run{project_basename}{i}.in') as file:
		acceptance_test_inputs.append(file.read())
	with open(f'Run{project_basename}{i}.out') as file:
		acceptance_test_outputs.append(file.read())
required_files.extend(acceptance_test_filenames)

group_submissions_path = 'group_JSON_submissions/*.json'

submissions = {}
emails = {}

# clone all gitlab repos
group_json_files = glob.glob(group_submissions_path)
num_files = len(group_json_files)
for i in range(num_files):
	filename = group_json_files[i]
	if filename[-12:] == '.schema.json':
		# ignore schema JSON files
		continue
	print(f'====================================\ncurrently checking group JSON file {filename} and cloning repository\nfile {i+1} out of {num_files} files')
	with open(filename, 'r') as f:
		try:
			data = json.load(f)['Project #2']
			gitlab_username = data['GitLab Username']
			emails[gitlab_username] = {
				'group_number': data['Group Number'],
				'email_1': data['Member #1 E-mail'],
				'email_2': data['Member #2 E-mail'],
				'eid_1': data['Member #1 EID'].lower(),
				'eid_2': data['Member #2 EID'].lower(),
				'member_1_full_name': f'{data["Member #1 First Name"]} {data["Member #1 Last Name"]}',
				'contents': ''
			}
		except Exception as e:
			print(f'Invalid json for {filename}')
			with open(f'{output_path}/invalidGroupJson.txt', 'a') as f:
				f.write(f'{filename} is a invalid json file\n{e}\n')
			continue
		
		# construct the `.git` string from the GitLab URL; if any part failed,
		# try directly cloning from the provided username's namespace
		chdir('repos')
		
		try:
			gitlab_url = data['GitLab URL']
			clone_url = gitlab_url.replace('https://gitlab.com/', 'git@gitlab.com:').replace('http://gitlab.com/', 'git@gitlab.com:')
			if clone_url[-1] == '/':
				clone_url = clone_url[:-1]
			if clone_url[-4:] != '.git':
				clone_url += '.git'
			subprocess.run(['git', 'clone', clone_url, gitlab_username], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
		except:
			try:
				clone_url = 'git@gitlab.com:' + gitlab_username + '/diplomacy.git'
				subprocess.run(['git', 'clone', clone_url, gitlab_username], capture_output=True, check=True)
			except Exception as e:
				stderr_string = e.stderr.decode("utf-8")
				if 'already exists' not in stderr_string:
					emails[gitlab_username]['contents'] += f'Error while trying to clone from repo {clone_url}:\n{stderr_string}\nPossible causes: forgetting to invite graders as maintainers, giving the incorrect GitLab username, etc.\n'
		
		submissions[gitlab_username] = data
		chdir('..')

gitlab_usernames = list(submissions.keys())

# HELPER FUNCTIONS START HERE
# =======================================================

# check git SHA; operates inside the `/repos/gitlab_username` folder
def check_SHA(gitlab_username):
	data = submissions[gitlab_username]
	# UTF-8 format; doesn't look like we need to specify this
	sha = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
	submitted_sha = data['Git SHA']
	if sha != submitted_sha:
		print(f'Submitted Git SHA does not match the private code repo\'s SHA for the latest commit for gitlab_username {gitlab_username}')
		emails[gitlab_username]['contents'] += f'Submitted Git SHA ({submitted_sha}) does not match the private code repo\'s SHA for the latest commit ({sha})\n'

# check all required files are present in private code repo
def check_required_files(gitlab_username):
	numNotFound = 0
	for item in required_files:
		if item not in glob.glob(item):
			numNotFound += 1
			notFoundMessage = f'{item} not found in private code repo'
			print(notFoundMessage)
			emails[gitlab_username]['contents'] += f'{notFoundMessage}\n'
			
# examine unit tests
# 1. make sure that it runs by trying the relevant `make` command
# 2. count the number of unit tests to make sure that there are enough
def checkUnitTests(gitlab_username):
	if 'makefile' not in glob.glob('makefile'):
		return
	if test_py_file not in glob.glob(test_py_file):
		return

	# run unit tests
	subprocess.run(['make', 'clean'], stdout=subprocess.DEVNULL)
	try:
		subprocess.run(['make', f'Test{project_basename}.tmp'], stdout=subprocess.DEVNULL)
	except:
		emails[gitlab_username]['contents'] += 'Unit tests failed\n'

	# count number of tests
	with open(test_py_file, 'r') as f:
		num_unit_tests = f.read().count('def test')
	# print(str(num_unit_tests) + ' unit tests found')
	if num_unit_tests < min_num_unit_tests:
		emails[gitlab_username]['contents'] += f'Insufficient unit tests: {num_unit_tests} unit tests found and a minimum of {min_num_unit_tests} is required\n'
		
# check submitted acceptance tests:
# 1. each runs successfully (does not error out or time out)
# 2. TODO: check that the acceptance tests themselves pass
acceptance_test_timeout = 20
def checkSubmittedAcceptanceTests(gitlab_username):
	if run_py_file not in glob.glob(run_py_file):
		return
	for filename in acceptance_test_filenames:
		if filename not in glob.glob(filename):
			return
	
	for i in range(1, num_acceptance_tests + 1):
		# try running the acceptance test
		filename = f'Run{project_basename}{i}.in'
		stdin = open(filename, 'r')
		try:
			subprocess.run(['python', run_py_file], stdin=stdin, stdout=subprocess.DEVNULL, timeout=acceptance_test_timeout)
		except subprocess.TimeoutExpired as e:
			print(f'student acceptance test {filename} timed out')
			emails[gitlab_username]['contents'] += f'student acceptance test {filename} timed out (more than {acceptance_test_timeout} seconds)\n'
		except Exception as e:
			emails[gitlab_username]['contents'] += f'Runtime Exception during student acceptance test {filename}:\n{e}\n'

# run our own acceptance tests
def runOurAcceptanceTests(gitlab_username):
	if run_py_file not in glob.glob(run_py_file):
		return
	
	num_failed_acceptanceTests = 0
	for i in range(1, num_acceptance_tests+1):
		try:
			output = subprocess.run(['python', run_py_file], input=acceptance_test_inputs[i-1], capture_output=True, timeout=acceptance_test_timeout, text=True).stdout
			
			# strip() to account for students outputting extra newlines in the end
			if output.strip() != acceptance_test_outputs[i-1]:
				# comment the following out as to NOT produce diff_message during vetting,
				# since the grader acceptance tests should remain hidden
				diff_message = f'Grader acceptance test {i} failed\n====\nreceived output:\n====\n{output}\n====\nintended output:\n====\n{acceptance_test_outputs[i-1]}\n====\n'
				emails[gitlab_username]['contents'] += diff_message
				emails[gitlab_username]['contents'] += f'Grader acceptance test {i} failed (incorrect output)\n'
				num_failed_acceptanceTests += 1
		except subprocess.TimeoutExpired as e:
			print(f'grader acceptance test {i} Timeout')
			emails[gitlab_username]['contents'] += f'{run_py_file} timed out on grader acceptance test number {i} (more than {acceptance_test_timeout} seconds)\n'
		except Exception as e:
			emails[gitlab_username]['contents'] += f'Runtime Exception during grader acceptance test number {i}: {e}\n'
	
	if num_failed_acceptanceTests > 0:
		emails[gitlab_username]['contents'] += f'Number of grader acceptance tests failed: {num_failed_acceptanceTests}\n'


# HELPER FUNCTIONS END HERE
# =======================================================

# perform all the checks of the code repos (SHA and required files)
chdir(base_path + '/repos')
num_submissions = len(gitlab_usernames)
for i in range(num_submissions):
	gitlab_username = gitlab_usernames[i]
	print(f'====================================\ncurrently checking private code repo files for {gitlab_username}\nsubmission {i+1} out of {num_submissions} submissions')
	# first try to get into the submission; skip if it doesn't exist
	# TODO: use `chdir()` and catch exception here for more modularity...?
	try:
		os.chdir(gitlab_username)
		# print(f'cd to {os.getcwd()}')
	except Exception as e:
		print(f'failed to enter this GitLab ID folder: {gitlab_username}\n{e}\nreturning to `/repos`')
		chdir(base_path + '/repos')
		continue
	
	check_SHA(gitlab_username)
	check_required_files(gitlab_username)
	checkUnitTests(gitlab_username)
	checkSubmittedAcceptanceTests(gitlab_username)
	runOurAcceptanceTests(gitlab_username)
	
	chdir(base_path + '/repos')

# check required files are in the test repo
chdir(base_path)
subprocess.run(['git', 'clone', 'git@gitlab.com:fareszf/cs330e-diplomacy-tests.git'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
chdir('cs330e-diplomacy-tests')
existing_filenames = list(map(lambda filename: filename.lower(), os.listdir()))

for i in range(num_submissions):
	gitlab_username = gitlab_usernames[i]
	print(f'====================================\ncurrently checking public test repo files for {gitlab_username}\nsubmission {i+1} out of {num_submissions} submissions')
	filenames = [
		f'{gitlab_username}-{test_py_file}',
		f'{gitlab_username}-{test_out_file}'
	]
	for acceptance_test_filename in acceptance_test_filenames:
		filenames.append(f'{gitlab_username}-{acceptance_test_filename}')
	for filename in filenames:
		if filename.lower() not in existing_filenames:
			print(filename + ' not found in the public test repo')
			emails[gitlab_username]['contents'] += f'{filename} is not found in the public test repo\n'
		
# print out emails and resubmit requests
chdir(output_path)
for email in emails.values():
	if email['contents'] == '':
		continue
	target_name = ''
	group_number = email['group_number']
	if group_number == '':
		target_name = email['member_1_full_name']
	else:
		target_name = f'Group {group_number}'
	with open('resubmitRequests.txt', 'a') as r:
		r.write(f'{target_name} ({email["eid_1"]} and {email["eid_2"]}) requested to resubmit\n')
	with open('email_output.txt', 'a') as o:
		o.write(f'{email["email_1"]}; {email["email_2"]}\n')
		o.write(f'Hello {target_name},\n\nBased on our vetting script, you had the following errors in your {project_basename} submission:\n\n{email["contents"]}\n\nYou may resubmit your project with additional late penalty counting from when the Piazza announcement becomes published (please check the Piazza announcement for details). If you do not resubmit, we will grade your existing submission without additional late penalty. If you decide to resubmit, please reply to this email after you finish resubmitting.\n\nPlease let me know if there is any mistake in the vetting script\'s output.\n\nThanks,\nPeter\n\n')
chdir(base_path)

