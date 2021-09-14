#!/usr/bin/python
# -*- coding: utf-8 -*
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: aws_ssm_instance
version_added: 1.0.0
short_description: Perform various System Manager instance tasks.
description:
    - This module allows the user to get SSM instance information or deregister an SSM instance
options:
  state:
    description
      - Specifies the state of the ssm instance. 
    required: true
    aliases: ['command']
    choices: ['deregister', 'get']
    type: str
  instance_id: 
    description:
      - The ID of the SSM instance
    required: false
    type: str
  region:
    description:
      - AWS Region
    required: true
    type: str
  filters:
    description:
      - A dict of filters to apply. Each dict item consists of a filter key and a filter value. See
        U(https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeInstances.html) for possible filters. Filter
        names and values are case sensitive.
    required: false
    default: {}
    type: dict
  instance_ids:
    description:
      - If you specify one or more instance IDs, only instances that have the specified IDs are returned.
    required: false
    type: list
    elements: str
author:
  - "Sergio Mejia (@sergio-gaggle)"
'''

EXAMPLES = '''
- hosts: localhost
  tasks:
  - name: deregister ssm instance
    local_action:
      module: gagglenet.ecs_anywhere.aws_ssm_instance
      state: deregister
      instance_id:  mi-0db497f1c7f0f903c

- hosts: localhost
  tasks:
  - name: get ssm instances
  local_action:
    module: gagglenet.ecs_anywhere_aws_ssm_instance
    state: get
'''

RETURN = '''
InstanceInformationList:
  description: List of instances information
  type: list
  returned: state is get
output:
  description: ssm operation output
  type: dict
  returned: state is delete
'''

try:
    import botocore
except ImportError:
    pass  # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.core import is_boto3_error_code
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import ansible_dict_to_boto3_filter_list


@AWSRetry.jittered_backoff()
def _describe_instances(connection, **params):
    paginator = connection.get_paginator('describe_instance_information')
    return paginator.paginate(**params).build_full_result()


def get_ssm_instance_info(module, client):
    instance_ids = module.params.get("instance_ids")
    filters = ansible_dict_to_boto3_filter_list(module.params.get("filters"))

    try:
        ssm_output = _describe_instances(client, Filters=filters)
    except is_boto3_error_code('InvalidActivationId') as e:
        module.warn("Could not find activation.")
    except (botocore.exceptions.BotoCoreError, botocore.exceptions.ClientError) as e:
        module.fail_json_aws(e, msg=e)
    module.exit_json(msg="SSM Activation List", output=ssm_output['InstanceInformationList'])


def deregister_ssm_instance(module, client):
    instance_id = module.params.get("instance_id")
    ssm_output = None

    try:
        ssm_output = client.deregister_managed_instance(
            InstanceId=instance_id
        )
    except is_boto3_error_code('InvalidInstanceId') as e:
        module.warn("Could not find instance.")
    except (botocore.exceptions.BotoCoreError, botocore.exceptions.ClientError) as e:
        module.fail_json_aws(e, msg=e)
    module.exit_json(msg="Deregistered SSM Instance", output=ssm_output, changed=True)


def main():
    argument_spec = dict(
        instance_id=dict(type='str'),
        state=dict(type='str', required=True, choices=['deregister', 'get'],
                   aliases=['command']),
        filters=dict(default={}, type='dict')
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        mutually_exclusive=[
            ['instance_ids', 'filters']
        ],
        supports_check_mode=True,
    )

    command = module.params['state']

    client = module.client('ssm')

    if command == 'deregister':
        deregister_ssm_instance(module, client)
    elif command == 'get':
        get_ssm_instance_info(module, client)

    module.exit_json(failed=False)


if __name__ == '__main__':
    main()
