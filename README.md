# Ansible Collection - gagglenet.ecsanywhere

## Role Summary

This role provides the following:

-   Installation of ecs and ssm agents and registers ssm node for AWS ECS Anywhere
-   Playbooks to register or deregister ssm nodes

Supports the following Operating Systems:

-   CentOS 7
-   CentOS 8

## Requirements

This role requires Ansible 2.4 or higher and AWS CLI v2.

## Variables

| variable | description | required? | default |
| -------- | ----------- | ---------- | ------- | 
| iam_role | Which IAM role to associate with instance | yes | - |
| aws_ecs_cluster | Name of ECS cluster to use | yes | - |
| aws_region | Which region to use for this ECS instance | yes | `us-west-2` |
| aws_install_dir | Where to install ECS anywhere | no | `/opt/amazon/ecs-anywhere` |
| aws_script_url | Location of install script | no | `https://amazon-ecs-agent.s3.amazonaws.com/ecs-anywhere-install-latest.sh` |


## Example Playbooks

Install ECS and SSM agents and register SSM node

```yaml
---
- hosts: aws_ecs
  tasks:
  - name: Run AWS Install Script
    include_role:
      name: gagglenet.ecs_anywhere.ecs_anywhere
      tasks_from: aws-script-install
    vars:
      iam_role: ecsAnywhereRole
      aws_ecs_cluster: ecs-anywhere
      region: us-west-2

```

## Running the Playbook
```bash
ansible-playbook ecs-anywhere.yml -i hosts 
```

## License

MIT

## Author Information
[gaggle-net](https://github.com/gaggle-net)
