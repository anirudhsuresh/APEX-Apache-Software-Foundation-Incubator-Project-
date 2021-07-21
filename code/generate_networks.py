# -*- coding: utf-8 -*-
"""
Created on 2020/6/11 18:45 
@author: Likang Yin
"""
import json
import networkx as nx
import numpy as np
from tqdm import tqdm
import csv
import re
import os

def match_id_alias_name_old(path):
    # match ID to aliases name
    # path should be aliases_2019_8.csv
    id_name_dict = {}
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        for item in reader:
            id_name_dict[item[0]] = item[2] # column 0: aliases id; column 2: name
    return id_name_dict

def dealising_old(s1, s2):

    s1, s2 = s1.lower(), s2.lower()
    #l1, l2 = len(s1), len(s2)

    '''
    if l1 == l2:
        if s1 == s2 or (s1.replace('.', ' ') == s2) or (s2.replace('.', ' ') == s1):
            return True
        return False
    '''

    #if l1 - l2 == -1:
    for i in range(len(s2)):
        if s1 == s2[:i] + s2[i+1:]:
            return True
    return False

    '''

    if l1 - l2 == 1:
        for i in range(l1):
            if s2 == s1[:i] + s1[i+1:]:
                return True
        return False
    '''

# A Dynamic Programming based Python program for 1-edit distance problem 
def dealising(str1, str2):

    str1, str2 = str1.lower(), str2.lower()

    m = len(str1)
    n = len(str2) 
    # Create a table to store results of subproblems 
    dp = [[0 for x in range(n + 1)] for x in range(m + 1)] 

    '''
    if m == n:
        if str1 == str2 or (str1.replace('.', ' ') == str2) or (str2.replace('.', ' ') == str1):
            return True
        return False
    if m > n:
        if str1[:-1] == str2 or str1[1:] == str2:
            return True
    '''
    #if m < n:
    if str2[:-1] == str1 or str2[1:] == str1:
        return True

    # Fill d[][] in bottom up manner 
    for i in range(m + 1): 
        for j in range(n + 1): 
  
            # If first string is empty, only option is to 
            # insert all characters of second string 
            if i == 0: 
                dp[i][j] = j    # Min. operations = j 
  
            # If second string is empty, only option is to 
            # remove all characters of second string 
            elif j == 0: 
                dp[i][j] = i    # Min. operations = i 
  
            # If last characters are same, ignore last char 
            # and recur for remaining string 
            elif str1[i-1] == str2[j-1]: 
                dp[i][j] = dp[i-1][j-1] 
  
            # If last character are different, consider all 
            # possibilities and find minimum 
            else: 
                dp[i][j] = 1 + min(dp[i][j-1],        # Insert 
                                   dp[i-1][j])        # Remove 
    if dp[m][n] == 1:
        return True
    else:
        return False

def match_id_alias_name(path):
    # match ID to aliases name
    # path should be aliases_2019_8.csv

    id_name_dict = {}
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        for item in reader:

            pid = item[0]
            full_name = item[2]
            alias = item[1].split('@')[0]
            person_id = item[3]
            length = len(alias)

            if length not in id_name_dict:
                id_name_dict[length] = []

            if '=' in full_name:

                if alias == 'jira' or 'noreply' in alias:
                    # return jira + id
                    id_name_dict[length].append([pid, alias + pid, alias, person_id, length])
                else:
                    id_name_dict[length].append([pid, alias, alias, person_id, length])
            
            elif '@' in full_name:
                id_name_dict[length].append([pid, full_name.split('@')[0], alias, person_id, length])

            else:
                id_name_dict[length].append([pid, full_name, alias, person_id, length])

    #print(id_name_dict['1'])
    #print(id_name_dict['15'])

    #raise KeyError
    
    #print(id_name_dict)


    key_list = list(id_name_dict.keys())
    key_list.sort()

    print(key_list)

    for key in key_list:
        print(len(id_name_dict[key]))

    rst = {}
    changed_dic = {}
    check_set = set()

    for len1 in tqdm(key_list):

        list1 = id_name_dict[len1]
        list2 = []

        if (len1 + 1) in key_list:
            list2 = id_name_dict[len1 + 1]

        for item1 in list1:
            pid1, full_name1, alias1, person_id1, length1 = item1
            rst[pid1] = full_name1

            for item2 in list2:
                pid2, full_name2, alias2, person_id2, length2 = item2

                if person_id1 == person_id2 or dealising_old(alias1, alias2):

                    if pid1 not in changed_dic:
                        changed_dic[pid1] =set()
                    if pid2 not in changed_dic:
                        changed_dic[pid2] =set()

                    changed_dic[pid1].add(pid2)
                    changed_dic[pid2].add(pid1) 

                    #value = max(name_list, key=len)

    reg=r'\(.*?\)'

    maxlength = 0
    maxDict = {}

    for key in changed_dic:
        length = len(changed_dic[key])
        maxlength = max(length, maxlength)
        if length not in maxDict:
            maxDict[length] = 0

        maxDict[length] += 1
        # rst[key] = changed_dic[key]
    print(maxDict)
    print(maxlength)
    raise KeyError


    for pid in rst:
        rst[pid] = re.sub(reg, '', rst[pid]).strip()

    return rst

'''
def match_id_alias_name(path):
    # match ID to aliases name
    # path should be aliases_2019_8.csv

    def dealising(s1, s2):

        s1, s2 = s1.lower(), s2.lower()

        l1, l2 = len(s1), len(s2)

        if l1 == l2:
            if s1 == s2 or (s1.replace('.', ' ') == s2) or (s2.replace('.', ' ') == s1):
                return True
            return False

        if l1 - l2 == -1:
            for i in range(l2):
                if s1 == s2[:i] + s2[i+1:]:
                    return True
            return False

        if l1 - l2 == 1:
            for i in range(l1):
                if s2 == s1[:i] + s1[i+1:]:
                    return True
            return False


    id_name_dict = {}
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        for item in reader:

            pid = item[0]
            full_name = item[2]
            alias = item[1].split('@')[0]
            person_id = item[3]
            length = len(alias)

            if '=' in full_name:

                if alias == 'jira' or 'noreply' in alias:
                    # return jira + id
                    id_name_dict[pid] = [pid, alias + pid, alias, person_id, length]
                else:
                    id_name_dict[pid] = [pid, alias, alias, person_id, length]
            
            elif '@' in full_name:
                id_name_dict[pid] = [pid, full_name.split('@')[0], alias, person_id, length]

            else:
                id_name_dict[pid] = [pid, full_name, alias, person_id, length]

    #print(id_name_dict)

    key_list = list(id_name_dict.keys())
    rst = {}

    check_set = set()

    reg=r'\(.*?\)'

    for key1 in tqdm(key_list):
        for key2 in key_list:
            if key2 in check_set: continue

            pid1, full_name1, alias1, person_id1, length1 = id_name_dict[key1]
            pid2, full_name2, alias2, person_id2, length2 = id_name_dict[key2]

            full_name1 = full_name1.capitalize()
            full_name2 = full_name2.capitalize()

            if abs(length1 - length2) >= 2:
                rst[pid1] = re.sub(reg, '', full_name1).strip()
                rst[pid2] = re.sub(reg, '', full_name2).strip()

            elif person_id1 == person_id2 or dealising(alias1, alias2):
                if len(full_name1) >= len(full_name2):
                    full_name = full_name1
                else:
                    full_name = full_name2

                rst[pid1] = re.sub(reg, '', full_name).strip()
                rst[pid2] = re.sub(reg, '', full_name).strip() 

            else:
                rst[pid1] = re.sub(reg, '', full_name1).strip()
                rst[pid2] = re.sub(reg, '', full_name2).strip()

        #print([rst[pid1]])
        check_set.add(key1)

    return rst
'''

def write_to_json_commit(path, prj_id, month, match_name):
    # edges to be returned
    edges_list = []
    commit_dict = {}

    # open the commits file
    with open(path, 'r') as f:
        commits = f.readlines()

    for commit in commits[1:]:
        commit_time, author, file = commit.replace('\n', '').split(',')
        if 'Git' in author:
            continue

        if (author +',' + file) not in commit_dict:
            commit_dict[author +',' + file] = 1
        else: commit_dict[author +',' + file] += 1
    for item in commit_dict.items():
        edges = []
        name = match_name[item[0].split(',')[0]]
        file_name = item[0].split(',')[1].split('.')[-1]    # 只保留后缀
        edges.append(name)
        edges.append(file_name)
        edges.append(item[1])
        edges_list.append(edges)
    with open('/data/Apachembox/demo/Apache_Incubator_Demo/final_network/p{}m{}_commit.json'.format(prj_id, month), 'w', encoding='utf-8') as f:
        json.dump(edges_list, f, ensure_ascii=False)

def get_edge_list_e(path):
    # edges to be returned
    edges_list = []
    # open the commits file
    with open(path, 'r') as f:
        emails = f.readlines()

    for email in emails[1:]:
        email_time, sender, respondent = email.replace('\n', '').split(',')
        edges_list.append([sender,respondent])
    return edges_list

def write_to_json(path_e, prj_id, month, id_name_match):
    e_data = []

    # e网络
    edges_list_e = get_edge_list_e(path_e)
    # if len(edges_list_e) < 1: print("warning: {}: no edges".format(path_e))
    sta_dict = {}  # 用来统计权重
    for e in edges_list_e:
        edge_name = str(e)
        sender = id_name_match[edge_name.split(',')[0].replace('[', '').replace("'", '').replace(' ', '')]

        receiver = id_name_match[edge_name.split(',')[1].replace(']', '').replace("'", '').replace(' ', '')]

        if 'Git' in sender or 'Git' in receiver:
            continue 

        if sender not in sta_dict:
            sta_dict[sender] = [receiver]
        else:
            sta_dict[sender].append(receiver)
        if receiver not in sta_dict:    # 元素必须在name里出现过
            sta_dict[receiver] = []

    for item in sta_dict.items():
        save_dict = {}
        save_dict['name'] = item[0]
        save_dict['imports'] = item[1]
        e_data.append(save_dict)
    # print(e_data)
    with open('/data/Apachembox/demo/Apache_Incubator_Demo/final_network/p{}m{}_email.json'.format(prj_id, month), 'w', encoding='utf-8') as f:
        json.dump(e_data, f, ensure_ascii=False)

father_path_e = '/data/Apachembox/zhuangzhi_code/relative_div/monthly_time/emails_monthly/'
father_path_c = '/data/Apachembox/zhuangzhi_code/relative_div/monthly_time/commits_monthly/'



'''
id_name_match = match_id_alias_name('aliases_2019_8.csv')

id_name_match_old = match_id_alias_name_old('aliases_2019_8.csv')

with open('id_name_match.json', 'w') as js:
	json.dump(id_name_match, js, indent =4)

with open('id_name_match_old.json', 'w') as js:
	json.dump(id_name_match_old, js, indent =4)

for key in id_name_match:
    if key not in id_name_match_old:
        continue

    if id_name_match[key] != id_name_match_old[key]:
        old = id_name_match_old[key]
        new = id_name_match[key]
        print('{} is changed to {}'.format(old, new))

print(len(id_name_match), len(id_name_match_old))

'''

with open('id_name_match_final.json', 'r') as f:
    id_name_match = json.load(f)

for key in id_name_match:
    this_name = id_name_match[key]

    if this_name.count(' ') == 1:
        first, last = this_name.split(' ')
        last = last.lower()
        firstL = first[:1].upper()
        id_name_match[key] = firstL + last

for prj in tqdm(os.listdir(father_path_e)):

    monthly_csv = os.listdir(father_path_e+prj)
    for f_csv in monthly_csv:
        path_e = father_path_e + prj + '/' + f_csv
        path_c = father_path_c + prj + '/' + f_csv
        write_to_json_commit(path_c, prj, f_csv[5:-4], id_name_match)
        write_to_json(path_e, prj, f_csv[5:-4], id_name_match)
