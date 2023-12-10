# Ansible Collection - gaggle_net.ecs_anywhere

## Role Summary

This role provides the following:

-   Installation of ecs and ssm agents and registers ssm node for AWS ECS Anywhere
-   Playbooks to register or deregister ssm nodes

Supports the following Operating Systems:

-   CentOS 7
-   CentOS 8
-   Almalinux 8

## Requirements

This role requires Ansible 2.4 or higher and AWS CLI v2.

## Variables

| variable | description | required? | default |
| -------- | ----------- | ---------- | ------- | 
| ecs_anywhere_iam_role | Which IAM role to associate with instance | yes | - |
| ecs_anywhere_aws_ecs_cluster | Name of ECS cluster to use | yes | - |
| ecs_anywhere_aws_region | Which region to use for this ECS instance | yes | `us-west-2` |
| ecs_anywhere_aws_install_dir | Where to install ECS anywhere | no | `/opt/amazon/ecs-anywhere` |
| ecs_anywhere_aws_script_url | Location of install script | no | `https://amazon-ecs-agent.s3.amazonaws.com/ecs-anywhere-install-latest.sh` |
| ecs_anywhere_use_sudo_for_local_tasks | Override default sudo behaviour for local tasks | no | true |
| ecs_anywhere_aws_sso_profile | SSO profile used to run local task | no | omit |
| ecs_anywhere_include_docker_role | Install docker as a dependnecy | no | when os = rhel8 |

## Example Playbooks

Install ECS and SSM agents and register SSM node

```yaml
---
- hosts: aws_ecs
  tasks:
  - name: Run AWS Install Script
    include_role:
      name: gaggle_net.ecs_anywhere.ecs_anywhere
      tasks_from: aws-script-install
    vars:
      ecs_anywhere_iam_role: ecsAnywhereRole
      ecs_anywhere_aws_ecs_cluster: ecs-anywhere
      ecs_anywhere_aws_region: us-west-2

```

## Running the Playbook
```bash
ansible-playbook ecs-anywhere.yml -i hosts
```

## License

MIT

## Author Information
[gaggle-net](https://github.com/gaggle-net)
