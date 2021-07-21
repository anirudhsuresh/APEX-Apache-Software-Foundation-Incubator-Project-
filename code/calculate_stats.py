import os
from tqdm import tqdm
import json
from datetime import datetime
from datetime import timedelta
import humanize




with open('project_info.json', 'r') as f:
    dic = json.load(f)

def get_commit_stats(path):

    with open(path, 'r') as f:
        lines = eval(f.readlines()[0])

    dev_set = set()
    number_commits = 0

    for dev, file, nums in lines:
        dev_set.add(dev)
        number_commits += nums

    return [number_commits, len(dev_set)]


def get_email_stats(path):

    with open(path, 'r') as f:
        devs = eval(f.readlines()[0])

    number_devs = len(devs)
    number_emails = 0

    for dev in devs:
        number_emails += len(dev['imports'])
            

    return [number_emails, number_devs]



path = '/data/Apachembox/demo/Apache_Incubator_Demo/final_network/'

project_month_dic = {}

for this_monthly_csv in tqdm(os.listdir(path)):

    monthly_csv = this_monthly_csv.replace('.json', '')
    project_month, filetype = monthly_csv.split('_')
    prj, month = project_month.split('m')
    prj = prj.replace('p', '')

    if prj not in project_month_dic:
        project_month_dic[prj] = []

    if month not in project_month_dic[prj]:
        project_month_dic[prj].append(month)

        if month == '0':
            print(this_monthly_csv)
            raise KeyError

for prj in project_month_dic:
    for month in project_month_dic[prj]:



    #for f_csv in monthly_csv:
        d = {}

        path_e = path + 'p'+ prj + 'm' + month + '_email.json'
        path_c = path + 'p'+ prj + 'm' + month + '_commit.json'


        num_commits, num_committers = get_commit_stats(path_c)
        num_emails, num_senders = get_email_stats(path_e)

        # commits and emails
        d['num_commits'], d['num_committers'] = num_commits, num_committers
        d['commit_per_dev'] = round(num_commits/num_committers, 2) if num_committers != 0 else 0
        d['num_emails'], d['num_senders'] = num_emails, num_senders
        d['email_per_dev'] = round(num_emails/num_senders, 2) if num_senders != 0 else 0

        # from project info
        d['incubation_time'] = dic[prj]['incubation_time'] 
        d['intro'] = dic[prj]['intro'] 
        d['start_time'] = dic[prj]['start_date']
        d['end_time'] = dic[prj]['end_date']
        d['status'] = dic[prj]['status']

        d['project_name'] = dic[prj]['project_name']
        d['sponsor'] = dic[prj]['sponsor']
        d['intro'] = dic[prj]['intro']
        d['link'] = dic[prj]['link']

        # humanize
        d['start_time'] = datetime.strptime(d['start_time'], "%m/%d/%Y")
        d['end_time'] = humanize.naturaldate(datetime.strptime(d['end_time'], "%m/%d/%Y"))

        this_month = int(month)
        d['from'] = humanize.naturaldate(d['start_time'] + timedelta(days=30*(this_month-1)))
        d['to'] = humanize.naturaldate(d['start_time'] + timedelta(days=30*this_month))

        d['start_time'] = humanize.naturaldate(d['start_time'])


        with open('/data/Apachembox/demo/Apache_Incubator_Demo/measures/p{}m{}.json'.format(prj, month), 'w', encoding='utf-8') as f:
            json.dump(d, f, indent = 4, ensure_ascii=False)