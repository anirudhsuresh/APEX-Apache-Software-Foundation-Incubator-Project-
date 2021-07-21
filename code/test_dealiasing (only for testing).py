def dealising_old(s1, s2):

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


# A Dynamic Programming based Python program for 1-edit distance problem 
def editDistDP(str1, str2):
    m = len(str1)
    n = len(str2) 
    # Create a table to store results of subproblems 
    dp = [[0 for x in range(n + 1)] for x in range(m + 1)] 
  
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

    return dp[m][n] 
 
s1 = 'elias'
s2 = 'eclias'
print(dealising_old(s1,s2)) 

print(editDistDP(s1, s2))
# This code is contributed by Bhavya Jain 

# dealising('aliases_2019_8.csv')

