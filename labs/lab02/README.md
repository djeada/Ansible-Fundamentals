# Lab 02 · Desired state, idempotence, and drift

Create a directory and managed file, predict a second run, and repair manual drift.

## Before you run

Complete lab 01. Read [playbooks](../../notes/playbooks.md). Run commands from the repository root with `.venv` active. Open [the reference playbook](playbook.yml) after making your prediction.

## Predict

Which tasks should change on the first run? What should the second run report?

## Run

```bash
ansible-playbook labs/lab02/playbook.yml --diff
ansible-playbook labs/lab02/playbook.yml --diff
cat .sandbox/lab02/managed.txt
```

## Observe

The file contains `Managed by Ansible.` followed by a newline. The second recap has `changed=0`, `failed=0`, and `unreachable=0`. The file mode is declared as `0644`.

## Experiment

Edit `.sandbox/lab02/managed.txt` in your editor to contain `manual drift`, then run:

```bash
ansible-playbook labs/lab02/playbook.yml --check --diff
cat .sandbox/lab02/managed.txt
ansible-playbook labs/lab02/playbook.yml --diff
```

The check predicts a repair while leaving your edit in place. The real run restores the declared contents.

## Explain

Idempotence applies to repeating the same desired state. Repair after drift is expected to report a change. `changed_when: false` would hide the report; it would not make an always-mutating operation idempotent.

Record your predicted result, actual recap, observed artifact, and one corrected assumption. An expected-failure experiment should be recorded as a successful test of a rejected input, not hidden with `ignore_errors`.

## Stretch

Add a second managed file and explain how its desired content and permissions are represented.

## Next

[Previous lab](../lab01/README.md) · [Next lab](../lab03/README.md) · [Notes index](../../notes/README.md)

Generated artifacts remain inside `.sandbox/`. To reset all course output, use the documented [cleanup command](../../README.md#reset) after saving anything you need.
