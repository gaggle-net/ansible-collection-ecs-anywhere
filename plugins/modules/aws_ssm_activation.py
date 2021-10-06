#!/usr/bin/python
# -*- coding: utf-8 -*

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r'''
---
module: aws_ssm
version_added: 1.1.0
short_description: Perform various System Manager management tasks.
description:
    - This module allows the user to create SSM activations. 
options:
  state:
    description
      - Specifies the state of the ssm activation. 
    required: true
    aliases: ['command']
    choices: ['present', 'absent', 'create', 'delete', 'get']
    type: str
  iam_role:
    description: 
      - The iam role that will be assigned to the managed instance. 
    type: str
  instance_name:
    description:
      - The name of the registered, managed instance as it will appear in the Amazon Web Services 
      Systems Manager console.
    required: false
    type: str
  registration_limit:
    description: 
      - Maximum number of managed instances to register. Default is 1
    required: false
    type: int
  instance_id: 
    description:
      - The ID of the activation
    required: false
    type: str
  region:
    description:
      - AWS Region
    required: true
    type: str
  tags:
    description:
      - Tags dict to apply to the managed instance
author:
  - "Sergio Mejia (@sergio-gaggle)"
'''

EXAMPLES = '''
- hosts: localhost
  tasks:
  - name: Create SSM Activation
    aws_ssm_activation:
      state: create
      iam_role: ecsAnywhereRole
      region: us-west-2
    
- hosts: localhost
  tasks:
  - name: Delete SSM Activation
    aws_ssm_activation:
      state: delete
      activation_id: 12345678
    
- hosts: localhost
  tasks:
  - name: Get SSM Activation
    aws_ssm_activation:
      state: get
'''

RETURN = '''
activation_id:
  description: SSM Activation Id
  type: string
  returned: state is create
activation_code: 
  description: SSM Activation Code
  type: string
  returned: state is create
activation_list:
  description: List of SSM Activations
  type: list
  returned: state is get
'''

try:
    import botocore
except ImportError:
    pass  # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.core import is_boto3_error_code


def create_ssm_activation(module, client, iam_role, registration_limit):
    if module.check_mode:
        module.exit_json(msg="CREATE ACTIVATION operation skipped - running in check mode", changed=True)
    try:
        ssm_activation = client.create_activation(
            IamRole=iam_role,
            RegistrationLimit=registration_limit,
        )
    except (botocore.exceptions.BotoCoreError, botocore.exceptions.ClientError) as e:
        module.fail_json_aws(e, msg=e)
    module.exit_json(msg="SSM Activation Created", activation_id=ssm_activation['ActivationId'],
                     activation_code=ssm_activation['ActivationCode'], changed=True)


def delete_ssm_activation(module, client, activation_id):
    if module.check_mode:
        module.exit_json(msg="DELETE ACTIVATION operation skipped - running in check mode", changed=True)
    try:
        ssm_output = client.delete_activation(
            ActivationId=activation_id
        )
    except is_boto3_error_code('InvalidActivation') as e:
        module.warn("Could not find activation.")
    except (botocore.exceptions.BotoCoreError, botocore.exceptions.ClientError) as e:
        module.fail_json_aws(e, msg=e)
    module.exit_json(msg="SSM Activation Deleted", changed=True)


def get_ssm_activation(module, client, activation_id):
    try:
        if activation_id != 'None':
            ssm_output = client.describe_activations(
                Filters=[
                    {
                        'FilterKey': 'ActivationIds',
                        'FilterValues': [activation_id]
                    }
                ]
            )
        else:
            ssm_output = client.describe_activations()
    except is_boto3_error_code('InvalidInstanceId') as e:
        module.warn("Could not find activation.")
    except (botocore.exceptions.BotoCoreError, botocore.exceptions.ClientError) as e:
        module.fail_json_aws(e, msg=e)
    module.exit_json(msg="SSM Activation List", output=ssm_output['ActivationList'])


def main():
    argument_spec = dict(
        iam_role=dict(type='str'),
        registration_limit=dict(type='int', default=1),
        state=dict(type='str', required=True, choices=['present', 'absent', 'create', 'delete', 'get'], aliases=['command']),
        activation_id=dict(type=str, default='None')
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=(
            ('state', 'present', ['iam_role']),
            ('state', 'create', ['iam_role']),
            ('state', 'delete', ['activation_id'])
        ),
    )

    iam_role = module.params.get('iam_role')
    registration_limit = module.params.get('registration_limit')
    activation_id = module.params.get('activation_id')

    if module.params['state'] in ('present',  'create'):
        command = 'create'
    elif module.params['state'] in ('absent', 'delete'):
        command = 'delete'
    elif module.params['state'] == 'get':
        command = 'get'

    client = module.client('ssm')

    if command == 'create':
        create_ssm_activation(module, client, iam_role, registration_limit)
    elif command == 'delete':
        delete_ssm_activation(module, client, activation_id)
    elif command == 'get':
        get_ssm_activation(module, client, activation_id)

    module.exit_json(failed=False)


if __name__ == '__main__':
    main()

