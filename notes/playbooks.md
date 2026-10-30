# Plays, tasks, and execution order

A playbook is a YAML list of plays. Each play selects inventory hosts and defines work. A task has a human-readable name, one module/action, module arguments, and optional execution directives such as `when`, `register`, `notify`, and `tags`.

```yaml
---
- name: Maintain an example file
  hosts: sandbox
  gather_facts: false
  tasks:
    - name: Declare the file contents
      ansible.builtin.copy:
        content: "Learning by inspection.\n"
        dest: "{{ training_root }}/example.txt"
        mode: '0644'
```

This complete illustrative play assumes the course sandbox already exists. The runnable labs include [shared preparation](../playbooks/guard.yml) and are the better starting point for experiments.

## YAML details that affect behavior

Use spaces, not tabs. A sequence item begins with `-`; a mapping entry uses `key: value`. Quote a value beginning with `{{ ... }}` so YAML treats it as a string expression. Quote file modes such as `'0644'`. Use `true` and `false` for booleans. Use a block scalar (`|`) for intentionally multiline text.

A valid YAML file can still be an invalid Ansible playbook. An unknown module, two action statements in one task, or a task placed at the wrong nesting level may fail later validation.

## Order across hosts

With the default `linear` strategy, Ansible runs a task across the active hosts in a batch before moving to the next task. Hosts can execute concurrently up to the fork limit. `serial` controls batch size; it does not mean each task is globally sequential across all hosts. Read [orchestration](orchestration.md) before changing strategy or delegation.

A useful play order is: validate inputs, prepare prerequisites, configure resources, run necessary handlers, then verify observable state. Separate verification from repair when you want to detect drift without fixing it first.

## Inspect the plan

```bash
ansible-playbook labs/lab12/playbook.yml --syntax-check
ansible-playbook labs/lab12/playbook.yml --list-hosts
ansible-playbook labs/lab12/playbook.yml --list-tasks
ansible-playbook labs/lab12/playbook.yml --list-tags
ansible-playbook labs/lab12/playbook.yml --check --diff
```

Check mode is a simulation whose usefulness depends on module support and existing state. It does not provision prerequisites that later tasks need. A clean sandbox may therefore fail a check of a multi-step workflow. After a real converge, this course checks warm check mode separately. See [testing](testing.md).

## Tags are selectors

Lab 12 has `configure` and `verify` task tags. Run it normally once, then use `--tags verify` to inspect without repairing the artifact. A typo in a tag can select no useful work, so inspect `--list-tasks` first.

Tags do not select a version of a role. Version a dependency using a collection/role requirement or a Git reference; use tags only for execution selection.

## Imports and includes

| Construct | When tasks are expanded | Useful consequence |
|---|---|---|
| `import_tasks` / `import_role` | Statically while parsing | Tasks are visible to static listing and inherit selection directives |
| `include_tasks` / `include_role` | Dynamically when execution reaches them | Runtime conditions and loops can control what is loaded |

Tags on a dynamic include select the include itself, not automatically every included task. Deliberately apply tags to included tasks or use `apply` where supported. Avoid relying on task listing alone to describe a dynamic workflow.

<details><summary>Self-check: if a late task fails, are earlier file changes undone?</summary>

No. Earlier tasks have already changed their targets. Recovery requires explicitly designed work, such as restoring a snapshot in a rescue block. See project 02.

</details>

Practice: [lab 02](../labs/lab02/README.md), [lab 12](../labs/lab12/README.md). Reference: [Playbook guide](https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_intro.html).
