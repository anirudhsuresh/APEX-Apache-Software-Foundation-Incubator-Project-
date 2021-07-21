import os
from tqdm import tqdm
import json



def get_committers(path):

    with open(path, 'r') as f:
        lines = eval(f.readlines()[0])

    dev_set = set()

    for dev, file, nums in lines:
        dev_set.add(dev)

    return dev_set


def get_commentors(path):

    with open(path, 'r') as f:
        devs = eval(f.readlines()[0])

    commentors_set = set()

    for dev in devs:
    	for dev_name in dev['imports']:
    		commentors_set.add(dev_name)
           
    return commentors_set


with open('project_info.json', 'r') as f:
    dic = json.load(f)

path = '/data/Apachembox/demo/Apache_Incubator_Demo/final_network/'

project_month_dic = {}

projects = os.listdir(path)

for this_monthly_csv in projects:

    monthly_csv = this_monthly_csv.replace('.json', '')
    project_month, filetype = monthly_csv.split('_')
    prj, month = project_month.split('m')
    prj = prj.replace('p', '')

    if prj not in project_month_dic:
        project_month_dic[prj] = []

    if month not in project_month_dic[prj]:
        project_month_dic[prj].append(month)

for prj in tqdm(project_month_dic):
    for month in project_month_dic[prj]:

    #for f_csv in monthly_csv:
        d = {}

        path_e = path + 'p'+ prj + 'm' + month + '_email.json'
        path_c = path + 'p'+ prj + 'm' + month + '_commit.json'


        committers_set = get_committers(path_c)

        commentors_set = get_commentors(path_e)

        this_dev_set = commentors_set.intersection(committers_set)

        with open(path_e, 'r') as f:
        	line_e = str(f.readlines()[0])

        with open(path_c, 'r') as f:
        	line_c = str(f.readlines()[0])

        for this_dev in this_dev_set:
        	line_e = line_e.replace(this_dev, this_dev + '*')
        	line_c = line_c.replace(this_dev, this_dev + '*')

        	#print(this_dev + '*')

        #print([len(committers_set), len(commentors_set), len(this_dev_set)])

        with open(path_e, 'w') as f:
        	f.write(line_e)

        with open(path_c, 'w') as f:
        	f.write(line_c)