#!/usr/bin/env python

import re
import json

facts = {}
facts['ceph_devs'] = []
devices = facts['ceph_devs']

def get_facts_from_config():
	data=open("/proc/partitions").readlines()[3:-1]

	for line in data:
		while '  ' in line:
			line = line.replace('  ', ' ')
		line = line.strip(' ')
		linelist = line.split()
		linelist = linelist[2:4]
		if int(linelist[0]) > 2500000000:
			if re.match ('^[a-z]{3,4}$', linelist[1]):
				devices.append(linelist[1])

	return facts

def main():
    module = AnsibleModule(argument_spec = dict())

    facts = get_facts_from_config()
    if facts:
        module.exit_json(ansible_facts=facts, changed=False)
    else:
        module.exit_json(changed=False)

# include magic from lib/ansible/module_common.py
#<<INCLUDE_ANSIBLE_MODULE_COMMON>>
main()
