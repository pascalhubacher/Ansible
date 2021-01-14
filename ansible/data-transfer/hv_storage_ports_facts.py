#!/usr/bin/python

# Copyright: (c) 2020, Your Name <YourName@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: hv_storage_facts

short_description: This module provides information about the Hitachi block storage system.

version_added: "0.9.0"

description: This is my longer description explaining my facts module.

options:
    storage_serial:
        description: This is the message to send to the test module.
        required: true
        type: int
    storage_ip_fqdn:
        description: This is the message to send to the test module.
        required: true
        type: str
    storage_port:
        description: This is the message to send to the test module.
        required: false
        type: str
    username:
        description: This is the message to send to the test module.
        required: true
        type: str
    password:
        description: This is the message to send to the test module.
        required: true
        type: str

author:
    - Pascal Hubacher (@pascalhubacher)
'''

EXAMPLES = r'''
- name: Testing Get Storage System
  hosts: localhost
  gather_facts: false
  vars:
    - storage_serial: 123456
    - storage_ip_fqdn: '192.168.0.1'
    - username: 'test'
    - password: 'test'
  tasks:
  - name: test the storage facts
    hv_storage_facts:
      storage_serial: '{{ storage_serial }}'
      storage_ip_fqdn: '{{ storage_ip_fqdn }}'
      username: '{{ username }}'
      password: '{{ password }}'
    register: result
  -name: output the result
  debug:
    msg: result
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
ansible_facts:
  description: Facts to add to ansible_facts.
  returned: always
  type: dict
  contains:
    foo:
      description: Foo facts about operating system.
      type: str
      returned: when operating system foo fact is present
      sample: 'bar'
    answer:
      description:
      - Answer facts about operating system.
      - This description can be a list as well.
      type: str
      returned: when operating system answer fact is present
      sample: '42'
'''

import json
#import the logging module to specify the logging level
import logging
import time
#import the HitachiBlockAPI functionality
from HitachiBlockAPI import RestAPI
#import the HitachiBlockAPI logger
from HitachiBlockAPI import logger

from ansible.module_utils.basic import AnsibleModule
#from ansible.module_utils.hv_log import Log
#from display

def run_module():
  # define available arguments/parameters a user can pass to the module
  module_args = dict(
      storage_serial=dict(type='int', required=True),
      storage_ip_fqdn=dict(type='str', required=True),
      storage_port=dict(type='str', required=False, default=None),
      username=dict(type='str', required=True),
      password=dict(type='str', required=True, no_log=True),
      logging_level=dict(type='str', required=False, default='DEBUG')
  )

    # seed the result dict in the object
  # we primarily care about changed and state
  # changed is if this module effectively modified the target
  # state will include any data that you want your module to pass back
  # for consumption, for example, in a subsequent task
  result = dict(
      changed=False,
      #original_message='Getting detailed information about the hitachi storage system',
      message='Getting detailed information about the hitachi storage system',
      data = None,
      time_used_sec=None
  )

  # the AnsibleModule object will be our abstraction working with Ansible
  # this includes instantiation, a couple of common attr would be the
  # args/params passed to the execution, as well as if the module
  # supports check mode
  module = AnsibleModule(
      argument_spec=module_args,
      supports_check_mode=True
  )

  #logger.setLevel(logging.INFO)
  if module.params['logging_level'] == 'DEBUG':
    logger.setLevel(logging.DEBUG)
  else:
    logger.setLevel(logging.INFO)

  # if the user is working with this module in only check mode we do not
  # want to make any changes to the environment, just return the current
  # state with no modifications
  if module.check_mode:
      module.exit_json(**result)
  try:
    start = time.time()
    #create storage object
    if module.params['storage_port'] == None:
      storage = RestAPI(fqdn_ip=module.params['storage_ip_fqdn'], username=module.params['username'], password=module.params['password'])
    else:
      storage = RestAPI(fqdn_ip=module.params['storage_ip_fqdn'], port=module.params['storage_port'], username=module.params['username'], password=module.params['password'])

    #set the storage with the specified serial to active
    storage.storage_device_id_set(serial_number=module.params['storage_serial'])

    #collect storage information
    #result['data'] = storage.storage_device_id_get()
    result['data'] = storage.ports_get(timeout=180)
    if result['data'] == -1 or result['data'] == None:
      module.fail_json(msg='Error - Timeout time not long enough.')

    result['time_used_sec'] = str((time.time()-start))
    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)
  except Exception as ex:
    module.fail_json(msg=ex.message)

def main():
  run_module()


if __name__ == '__main__':
  main()