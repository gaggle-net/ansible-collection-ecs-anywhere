# Ansible Collection - gagglenet.ecsanywhere

## Role Summary

This role provides the following:

-   Installation of ecs and ssm agents and registers ssm node for AWS ECS Anywhere
-   Playbooks to register or deregister ssm nodes

Supports the following Operating Systems:

-   CentOS 7
-   CentOS 8
-   Fedora 27 
-   Fedora 28

## Requirements

This role requires Ansible 2.4 or higher and AWS CLI v2. 

## Example Playbooks

Install ECS and SSM agents and register SSM node

```yaml
---
- hosts: aws_ecs
  tasks:
    - import_role:
        name: gagglenet.ecs_anywhere.ecs_anywhere
  become: yes
```

## Running the Playbook
```bash
ansible-playbook ecs-anywhere.yml -i hosts --extra_vars "aws_profile=int-con ssm_role=ecsAnywhereRole ecs_cluster=ecsAnywhere-test aws_region=us-west-2"
```

## License

Apache 2.0

## Author Information
[gaggle-net](https://github.com/gaggle-net)
