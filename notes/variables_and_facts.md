# Variables, facts, and results

A variable is input or intermediate data addressed by name. A fact is discovered host information. A registered result is the response from a task. These can all be accessed in expressions, but they answer different questions.

| Data | Example | Question it answers |
|---|---|---|
| Inventory input | `course_environment` | What environment should this host use? |
| Role default | `training_site_title` | What is the fallback for this role's interface? |
| Gathered fact | `ansible_facts['system']` | What system did the target report? |
| Registered result | `course_write.changed` | What did this task report on this host? |
| Derived host variable | A value from `set_fact` | What did this play calculate for this host? |

## A practical precedence model

Ansible has a detailed precedence order; do not memorize a shortened list as a complete specification. For the course's common **variable** sources, role defaults are easily overridden, inventory variables supply host/environment data, play variables override those, and `--extra-vars` overrides other variable values. Role parameters, task variables, facts, includes, and variable plugins add detail beyond this subset.

Playbook keywords, command-line options, variables, and configuration settings also have distinct precedence categories. For example, `ansible_user` is a connection variable and can override the `-u` command-line option. When debugging, first identify the category, then the variable source.

```bash
ansible-playbook labs/lab03/playbook.yml
ansible-playbook labs/lab03/playbook.yml -e course_environment=staging
ansible-inventory --host localhost
```

The inventory inspection shows inventory-derived values; it does not predict every play-, task-, or extra-variable override in a later playbook run.

## Types and expressions

Use native YAML or JSON when types matter:

```bash
ansible-playbook labs/lab06/playbook.yml -e '{"course_port": 9090}'
```

By contrast, `-e course_port=9090` supplies a string. Lab 06 deliberately rejects it with `course_port is integer`. This catches an invalid interface instead of silently guessing the intended type.

A `when` expression is already an expression; do not wrap it in `{{ }}`. Prefer comparisons or explicit type checks that yield booleans:

```yaml
# Task fragment
- name: Explain Linux-only behavior
  ansible.builtin.debug:
    msg: This host reports Linux.
  when: ansible_facts['system'] == 'Linux'
```

Modern core versions reject conditionals that produce non-boolean values. Convert a deliberately string-based yes/no input with `| bool` only when the accepted input contract warrants it. Do not use `default` to hide a required missing value; assert the requirement early.

## Facts are collected data

`gather_facts: true` runs fact gathering at play startup. Use `ansible_facts['...']` rather than relying on injected top-level names. Facts can be stale if cached, unavailable if gathering was disabled, or expensive if you collect more than needed. Do not write timestamps and other volatile facts into managed configuration unless the change is intentional.

## Results belong to hosts

`register: course_write` captures a task's result for each host. A loop usually produces a result with a `results` list, containing per-item results. A skipped task can still create a registered result with skip metadata; fields such as `stdout` may be absent. Inspect the structure before indexing it.

`set_fact` defines host variables during execution. Its default lifetime is the current run; fact caching changes what can persist across runs and introduces additional precedence considerations. Avoid overwriting a role input with `set_fact` just to shorten an expression.

<details><summary>Self-check: why is a host's inventory value different from the value printed inside a play?</summary>

A higher-precedence source may have overridden it: inspect play/task variables, role parameters, included vars, and extra vars. Also confirm you are reading the intended host and inventory. Inventory inspection alone cannot reveal all runtime overrides.

</details>

Practice: [lab 03](../labs/lab03/README.md), [lab 04](../labs/lab04/README.md), [lab 05](../labs/lab05/README.md). References: [Variables](https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_variables.html), [precedence categories](https://docs.ansible.com/projects/ansible/latest/reference_appendices/general_precedence.html), [2.19 templating changes](https://docs.ansible.com/projects/ansible/latest/porting_guides/porting_guide_core_2.19.html).
