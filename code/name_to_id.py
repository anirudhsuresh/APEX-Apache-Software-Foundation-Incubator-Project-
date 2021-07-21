import json
import os

with open('project_info.json', 'r') as f:
	project_info = json.load(f)

csvs = os.listdir('/data/Apachembox/demo/Apache_Incubator_Demo/final_network/')

cnt = 0
project_list = set()

for csv in csvs:
	pid = csv.split('m')[0].replace('p', '')
	project_list.add(pid)
	
name_to_id = {}

project_name_list = set()

for pid in project_info:
	status = project_info[pid]['status']
	project_name = project_info[pid]['project_name']
	project_name = project_name + ' [' + status + ']'
	project_name = project_name.capitalize()

	name_to_id[project_name] = pid
	if pid in project_list:
		project_name_list.add(project_name)

project_name_list = list(project_name_list)

for i in range(len(project_name_list)):
	project_name_list[i] = project_name_list[i]  

project_name_list = sorted(project_name_list)



for p in project_name_list:
	print('<option value="{}"/>'.format(p))

print(len(project_name_list))		


with open('name_to_id.json', 'w') as f:
	json.dump(name_to_id, f, indent = 4)








