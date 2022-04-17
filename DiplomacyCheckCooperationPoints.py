import os
import glob
import json
import time

# `base_path` must be absolute path; assuming running in Git Bash on Windows
# make sure to run after `make clean`
base_path = 'D:/Libraries Type-D/Documents/SCHOOL/UT Austin/Spring 2022/CS 330E Elements of Software Engineering (TA)/Projects/cs330e-diplomacy-grading-script'
output_path = 'output'
output_filename = 'bad_cooperation_list.txt'
submissions_path = 'evaluation_JSON_submissions/*.json'

def chdir(new_dir):
	try:
		os.chdir(new_dir)
		# print(f'cd to {os.getcwd()}')
	except Exception as e:
		print(f'cd to {new_dir} failed. Exception message:\n{e}')

submissions = {}
output_string = ''

# first, cd to the base_path and make the directory if necessary
chdir(base_path)
if not os.path.exists(output_path):
	os.makedirs(output_path)

# clone all gitlab repos
evaluation_json_files = glob.glob(submissions_path)
num_files = len(evaluation_json_files)
for i in range(num_files):
	filename = evaluation_json_files[i]
	print(f'====================================\ncurrently checking evaluation JSON file {filename}\nfile {i+1} out of {num_files} files\n====================================')
	with open(filename, 'r') as f:
		try:
			data = json.load(f)['Project #2']
			# only proceed if the cooperation points assignment is not the maximum
			assigned_points = data['Member #2 Cooperation Points']
			if assigned_points == 20:
				continue
			
			current_student_name = f'{data["First Name"]} {data["Last Name"]}'
			target_student_name = f'{data["Member #2 First Name"]} {data["Member #2 Last Name"]}'
			
		except Exception as e:
			print(f'Invalid json for{filename}')
			with open(f'{output_path}/invalidEvaluationJson.txt', 'a') as f:
				f.write(f'{filename} is a invalid json file\n{e}\n')
			continue
		
		output_string += f'{current_student_name} only assigned {assigned_points} points to {target_student_name}!\n'
		

# print out emails and resubmit requests
chdir(output_path)
with open(output_filename, 'w') as output_file:
	output_file.write(output_string)

chdir(base_path)

