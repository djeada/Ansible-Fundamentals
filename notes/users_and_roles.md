# Users, privileges, and reusable roles

The word “role” can mean a permission in an access-control system, but an **Ansible role** is a directory of reusable automation. It is not an operating-system user, an SSH account, or a sudo permission.

## Four identities to distinguish

| Identity | Where it exists | What controls it |
|---|---|---|
| Controller user | Your machine, running `ansible-playbook` | Your shell session and local file permissions |
| Connection user | Managed host, accepting SSH or another transport | `ansible_user`, connection configuration, authentication |
| Become user | Managed host, after privilege escalation | `become`, `become_user`, escalation policy and credentials |
| Managed account | A user resource you create or edit | A task such as `ansible.builtin.user` |

Setting `become_user: root` alone does not enable escalation. `become: true` enables it; the connection user still needs an authorized mechanism such as sudo. With a local connection, the controller's local account executes tasks unless escalation is explicitly enabled. The course does not enable it.

## User management is a system mutation

Illustrative task fragment for a disposable Linux VM only:

```yaml
- name: Add an application account to an existing group
  ansible.builtin.user:
    name: courseapp
    system: true
    create_home: false
    groups: developers
    append: true
  become: true
```

The group must already exist. `append: true` preserves other supplementary group memberships; without it, `groups` may replace them. Account deletion, home-directory removal, sudo policy, and password hashes need separate review. Never experiment with these tasks on your personal login account.

## A role exposes an interface

The [training_site role](../roles/training_site/tasks/main.yml) owns one behavior: render an HTML learning page. Its defaults define inputs; its tasks validate them and render a template. Lab 08 and project 01 reuse the same role.

| Role path | Purpose |
|---|---|
| `defaults/main.yml` | Low-precedence public input defaults |
| `tasks/main.yml` | Main task entry point |
| `templates/` | Jinja templates |
| `files/` | Static assets, when needed |
| `handlers/main.yml` | Change-triggered tasks, when needed |
| `vars/main.yml` | Higher-precedence internal variables, used sparingly |
| `meta/argument_specs.yml` | Optional formal argument validation |
| `meta/main.yml` | Optional metadata and dependencies |

A small role does not need every directory. Prefer a few clear inputs prefixed with the role name, sensible defaults, and observable outputs. Put configurable values in defaults rather than using `vars/main.yml` to make them difficult to override.

## Reuse and versioning

Roles can depend on or include other roles. The question is whether the dependency is explicit, bounded, documented, and testable. Avoid hidden cross-role variables and surprising side effects. A role may be worthwhile for organization and testing even when only one current play uses it.

Task tags control selection. Git tags, release versions, or dependency requirement versions control code versions. A task tag named `v2` does not install version 2 of a role.

A collection packages roles, plugins, and modules under a namespace. The course uses only builtin modules and a repository-local role; external collections are an optional extension. Pin and review any dependency you add.

<details><summary>Self-check: does adding roles: [training_site] give the connection user more privileges?</summary>

No. It loads reusable tasks and associated resources. Privilege escalation is separately controlled by `become` and the managed system's policy.

</details>

Practice: [lab 08](../labs/lab08/README.md), [project 01](../projects/01-learning-site/README.md). Reference: [Roles](https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_reuse_roles.html), [privilege escalation](https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_privilege_escalation.html).
