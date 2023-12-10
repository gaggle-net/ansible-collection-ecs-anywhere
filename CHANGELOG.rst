=====================================
Gaggle_Net.Ecs_Anywhere Release Notes
=====================================

.. contents:: Topics


v1.2.0
======

Release Summary
---------------

- Added options to override default role behaviors for environments not using the VSCode dev container.
- Optional variable to provide AWS SSO profile for running activation
- Introduced conditional dependency on the geerlingguy.docker role for EL8 based setups, following AWS ECS agent setup guidelines.
- Resolved issue reported for fixing syntax error in `tasks/deregister-ssm-instance.yml`.
- Syntax improvements as identified by ansible-lint and flake8 for code quality.
- Added a changelog.

