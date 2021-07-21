import os
import json


with open('/data/Apachembox/demo/id_name_match_old.json', 'r') as f:
	old = json.load(f)

with open('/data/Apachembox/demo/id_name_match.json', 'r') as f:
	new = json.load(f)

update= {}

for key in new:

	alias = new[key]
	for i in range(len(alias)):
		if alias[i] == ' ':
			new_alias = alias[:i] + ' ' + alias[i+1:].capitalize()
			print('{} is changed to {}'.format(alias, new_alias))
			alias = new_alias

	update[key] = alias.capitalize()


for key in update:
	if update[key] != new[key]:
		print('{} is changed to {}'.format(old[key], update[key]))

print([len(set(old.values())), len(set(new.values())), len(set(update.values()))])


with open('/data/Apachembox/demo/id_name_match_final.json', 'w') as f:
	json.dump(update, f, indent = 4)



















