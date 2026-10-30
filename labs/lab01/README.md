# Lab 01 · Control node, inventory, and module execution

Trace the selected host, connection, interpreter, and module. Distinguish an Ansible ping from an ICMP or HTTP probe.

## Before you run

Complete the root README installation. Read [the introduction](../../notes/intro.md) and [inventory notes](../../notes/inventory.md). Run commands from the repository root with `.venv` active. Open [the reference playbook](playbook.yml) after making your prediction.

## Predict

Will this play open an SSH connection? Which machine runs the test module?

## Run

```bash
ansible-inventory --graph
ansible sandbox --list-hosts
ansible sandbox -m ansible.builtin.ping
ansible-playbook labs/lab01/playbook.yml
```

## Observe

The graph contains `sandbox` and `localhost`. The ping result contains `pong`. The debug message identifies the local connection and virtual-environment Python. Sandbox preparation may change the directory mode on the first run; a repeat should have zero changes.

## Experiment

Compare the normal inventory with the two aliases below. This is inspection only:

```bash
ansible-inventory -i inventories/simulated/hosts.yml --graph
ansible sandbox --list-hosts --limit does_not_exist
```

The last command selects no hosts. Explain why an empty selection is not evidence that a system is configured.

## Explain

The explicit local connection avoids SSH. A successful ping proves module execution with the configured Python. It does not test an application. `inventory_hostname` is a logical name, and two aliases can refer to one computer.

Record your predicted result, actual recap, observed artifact, and one corrected assumption. An expected-failure experiment should be recorded as a successful test of a rejected input, not hidden with `ignore_errors`.

## Stretch

Add a debug message that distinguishes the inventory alias from the local system hostname.

## Bash alternative

Run [the self-contained Bash implementation](alternative.sh) with Bash 3.2+ and standard Unix utilities. It does not require Ansible, Python, jq, or a virtual environment. Follow the [shared Bash guide](../../notes/bash_alternatives.md) for input mappings, change reporting, and boundaries. Its output is separate from the Ansible track.

```bash
bash labs/lab01/alternative.sh
bash labs/lab01/alternative.sh --check
```

The script declares one logical local host and reports the executing Bash version. It does not parse Ansible inventory, connect through SSH, or run a Python ping module. Trace the local process instead of treating the printed success message as an application probe.

A stable repeat reports `SUMMARY changed=0 check=false`. `--check` predicts this script’s supported changes without writing them; it is an explicitly implemented preview, not Ansible check mode. Adapt this lab’s prediction and drift experiment to the Bash artifact before comparing both implementations.

## Next

[Course start](../../README.md) · [Next lab](../lab02/README.md) · [Notes index](../../notes/README.md)

Generated artifacts remain inside `.sandbox/`. To reset all course output, use the documented [cleanup command](../../README.md#reset) after saving anything you need.
