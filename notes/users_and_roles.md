# Users and Roles Management

Managing users and roles effectively is crucial for maintaining system security, consistency, and ease of administration across multiple servers. Ansible provides powerful mechanisms to manage users and roles, simplifying repetitive tasks across numerous machines.

TODO:

- WHAT ARE THOSE USERS??? WHERE FOR RUNNING PLAYBOOK?? OR WHAT?

## User Management with Ansible

Managing users includes creating, updating, and deleting users, as well as managing user privileges and group memberships.

### Creating Users

To create a user, the `user` module in Ansible is used. Consider this command:

```yaml
- name: Create a new user
  user:
    name: alice
    state: present
    shell: /bin/bash
    groups: sudo,developers
```

This task will:

- Ensure the user `alice` exists on the target system.
- Assign `/bin/bash` as the default shell.
- Add `alice` to the groups `sudo` and `developers`.

### Interpreting Results

Example output:
```
changed: [server1]
```
Interpretation:
- `changed`: Indicates a new user was created or updated as per the provided details.

### Modifying Existing Users

The same `user` module allows modifications, such as changing user groups or updating passwords:

```yaml
- name: Update user's group
  user:
    name: alice
    groups: admin
    append: yes
```

This will append `alice` to the `admin` group without removing existing group memberships.

Output example:
```
changed: [server1]
```
Interpretation:
- Confirms changes were made to group memberships for `alice`.

### Deleting Users

To delete a user:

```yaml
- name: Remove user
  user:
    name: alice
    state: absent
    remove: yes
```

Output example:
```
changed: [server1]
```
Interpretation:
- Confirms deletion of user `alice` and removal of the home directory.

## Role Management in Ansible

Ansible roles are structured ways to organize playbooks. Roles simplify complex tasks by encapsulating related tasks and variables, enhancing readability and reusability.

### What are Roles?

Roles should be for:

- easy re usability and prevent repeating yourself writing the same tasks over and over.

- bundling up individual tasks into 1 placeholder which later can be called from a playbook.

- roles should use tags. Why? when calling roles from other places you can point to a specific version of the role you know works whilst also promoting further development of such role.


Roles shouldn't be:

- stuff you won't need to repeat ever

- tasks that could be playbooks and default role vars that could be part of an actual vars or host_vars

- building blocks for other future roles. Roles should be isolated tasks for a specific use case.

Simple roles don’t bother me, but roles calling other roles does. If you start with the assumption that your automation code should be tested and versioned, it becomes easier to explain limiting dependencies.

A role that does a simple thing is easy to test. A role that calls two other roles is not.

Putting things into roles with sensible defaults also presents a kind of API between different aspects of a system.. If you change something substantial in a play, you will have to remember to run it on all relevant hosts(and maybe even know which ones they are).. If there are dependencies between plays, you'll have to memoise them..

If you change a variable name in a role however, you can find out if and where it breaks by doing a simple search, creating a role dependency tree or just by running in check mode.

### Basic Structure of an Ansible Role

A role typically has the following directory structure:

```
roles/
└── my_role
    ├── tasks
    │   └── main.yml
    ├── handlers
    │   └── main.yml
    ├── templates
    │   └── config.j2
    ├── files
    └── defaults
        └── main.yml
```

- `tasks/main.yml`: Contains the main tasks that execute when the role is invoked.
- `handlers/main.yml`: Tasks triggered by specific conditions (e.g., service restarts).
- `templates/`: Holds Jinja2 template files for dynamic configuration.
- `files/`: Contains static files to copy onto target systems.
- `defaults/main.yml`: Defines default variables for the role.

### Creating and Using Roles

To use a role in a playbook:

```yaml
- hosts: webservers
  roles:
    - my_role
```

Output example:

```
TASK [my_role : Install required packages] *********
changed: [server1]
```

Role executed and made changes on the specified host(s).

### Role Variables

Roles can have variables, defined in `defaults/main.yml`, which allow dynamic configuration:

```yaml
# defaults/main.yml
package_list:
  - nginx
  - php-fpm
```

Use variables in tasks:

```yaml
# tasks/main.yml
- name: Install packages
  apt:
    name: "{{ package_list }}"
    state: present
```

### Mathematical Model for Scaling Role Applications

To assess the efficiency of role execution over multiple hosts, we can use a simple linear model. Let $T(n)$ represent the total time taken to run a role across $n$ servers:

\[T(n) = t_{setup} + n \cdot t_{exec}\]

- $t_{setup}$: Initial setup time (constant overhead).
- $t_{exec}$: Execution time per server (average).

Example:

If $t_{setup} = 2\,\text{s}$ and $t_{exec} = 5\,\text{s}$, then for $n = 10$ servers:

\[T(10) = 2\,\text{s} + 10 \cdot 5\,\text{s} = 52\,\text{s}\]

This equation helps estimate performance and planning for large-scale role applications.

### Visual Diagram of Ansible Role Execution Flow

```
+-------------+
| Playbook    |
+-------------+
      |
      v
+-------------+
| Role        |
+-------------+
      |
      v
+-------------+        +-----------------+
| Tasks       |------->| Handlers        |
+-------------+        +-----------------+
      |
      v
+-------------+
| Templates   |
+-------------+
      |
      v
+-------------+
| Target Host |
+-------------+
```

- The playbook invokes the role.
- Role tasks execute in sequence.
- Tasks may trigger handlers (conditional tasks).
- Templates generate configuration files.
- Results apply to the target host.

