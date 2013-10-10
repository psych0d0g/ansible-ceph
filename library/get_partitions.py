#!/usr/bin/env python

import re
import json
import subprocess

facts = {}
devices = facts['ceph_devs'] = []
cephlist = []

def run_command(command):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')

def get_facts_from_config():
    data=open("/proc/partitions").readlines()[3:-1]

    for line in data:
        while '  ' in line:
            line = line.replace('  ', ' ')
        line = line.strip(' ')
        linelist = line.split()
        linelist = linelist[2:4]
        if int(linelist[0]) > 3000000000:
            if re.match ('^[a-z]{3,4}$', linelist[1]):
                cephlist.append(linelist[1])

	for line in run_command("/usr/sbin/ceph-disk list"):
	    if 'ceph data' in line:
	        if 'active' not in line:
	            for device in cephlist:
	                if device in line:
	                    devices.append(line)

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