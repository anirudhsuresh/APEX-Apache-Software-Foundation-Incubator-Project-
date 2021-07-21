import json
import csv 
import os

path = '/data/Apachembox/demo/lists_2019_8.csv'
dic = {}

with open(path, 'r') as f:
	lines = csv.reader(f)

	for line in lines:

		listid,listname,pj_alias,status,start_date,end_date,sponsor,intro,pj_url,pj_github_url = line
		if listid == 'listid': continue

		dic[listid] = {}

		dic[listid]['project_name'] = listname
		dic[listid]['start_date'] = start_date
		dic[listid]['end_date'] = end_date

		if status == '0':
			dic[listid]['status'] = 'Incubating'
			dic[listid]['end_date'] = 'In Progress'
		if status == '1':
			dic[listid]['status'] = 'Graduated'
		if status == '2':
			dic[listid]['status'] = 'Retired'

		dic[listid]['sponsor'] = sponsor
		dic[listid]['intro'] = intro
		dic[listid]['link'] = pj_url

		e_path = '/data/Apachembox/zhuangzhi_code/relative_div/monthly_time/emails_monthly/' + listid
		c_path = '/data/Apachembox/zhuangzhi_code/relative_div/monthly_time/commits_monthly/' + listid
		e_month, c_month = 1, 1

		if os.path.exists(e_path):
			e_month = len(os.listdir(e_path))
		if os.path.exists(c_path):
			c_month = len(os.listdir(c_path))

		dic[listid]['incubation_time'] = max(e_month, c_month)


with open('project_info.json', 'w') as f:
	json.dump(dic, f, indent= 4)


