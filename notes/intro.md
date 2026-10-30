# Ansible's execution model

Ansible coordinates work from a **control node**. An **inventory** supplies host names, groups, and connection variables. A **play** selects hosts; its **tasks** invoke modules to inspect or change each selected host. A playbook is a YAML list of plays.

For ordinary POSIX managed hosts, Ansible commonly connects over SSH and runs Python module code on the target. The target usually needs Python and a reachable account; it does not normally need an Ansible agent or installation. Network devices, Windows, API modules, and connection plugins have their own requirements.

In this course, `ansible_connection: local` makes your computer both controller and target. No SSH authentication occurs. Two inventory aliases pointing at this computer still share its filesystem and processes.

## State before steps

A shell script might say “append this line.” A configuration task should usually say “this file must contain these bytes.” That distinction lets a module compare current state with desired state and report whether it changed anything.

```yaml
# Task fragment: this directory must exist with a known mode.
- name: Create an application directory
  ansible.builtin.file:
    path: "{{ training_root }}/example"
    state: directory
    mode: '0755'
```

The first run may create the directory. The second run should observe the correct state. If someone removes it, the next run should recreate it. This is **convergence**. A task is **idempotent** when repeating the operation with the same inputs does not keep changing the resulting state.

Ansible does not automatically make arbitrary commands idempotent. A command that appends a line or restarts a service on every run still does so unless you design a guard or use a state-aware module. A green recap also does not prove the application works; verify the observable contract.

## Reading a result

| Status | What it tells you | What it does not prove |
|---|---|---|
| `ok` | The task completed without a reported change | The whole application is healthy |
| `changed` | The module reports a state change, or predicts one in check mode | The change was necessary or correct |
| `skipped` | A condition, tag selection, or execution mode omitted work | The desired state already exists |
| `failed` | Task execution reported an error | Earlier tasks were rolled back |
| `unreachable` | Ansible could not establish/use the required connection | A `rescue` block will recover the host |
| `rescued` | A task failure entered a successful recovery path | The original operation succeeded |

## A useful division of responsibilities

Use configuration modules for packages, files, users, and services. Use orchestration tasks for ordering and coordination. Use a command when there is no suitable module, but define its success and change conditions. Keep business data transformations in tools designed for that data rather than hiding them in a long shell pipeline.

Provisioning infrastructure, configuring it, and deploying an application are separate responsibilities even when one tool can perform all three. Decide which system owns each resource so that two automation tools do not continually undo each other's work.

## Try and explain

Run [lab 01](../labs/lab01/README.md), then [lab 02](../labs/lab02/README.md). Predict what will happen after manually editing the managed file.

<details><summary>Self-check: does a successful ping prove the web server is running?</summary>

No. `ansible.builtin.ping` checks that Ansible can execute its Python test module through the configured connection. It is not ICMP ping and does not test an HTTP service. Use an appropriate service or application-level probe for that contract.

</details>

Reference: [How to build your inventory](https://docs.ansible.com/projects/ansible/latest/inventory_guide/intro_inventory.html).
