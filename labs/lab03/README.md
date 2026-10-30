# Lab 03 · Variables, extra vars, and registered results

Trace inventory inputs, override an environment, and inspect a module result without confusing it with an input.

## Before you run

Complete lab 02. Read [variables and facts](../../notes/variables_and_facts.md). Run commands from the repository root with `.venv` active. Open [the reference playbook](playbook.yml) after making your prediction.

## Predict

Will changing an extra variable change the inventory file? Which result field tells you whether copy wrote anything?

## Run

```bash
ansible-playbook labs/lab03/playbook.yml
ansible-playbook labs/lab03/playbook.yml -e course_environment=staging
cat .sandbox/lab03/variables.json
ansible-playbook labs/lab03/playbook.yml -e course_environment=staging
```

## Observe

The JSON environment is `staging`. The inventory file remains unchanged. `course_write.changed` is true for a new rendered value and false when the same inputs are repeated.

## Experiment

Run the following deliberate invalid-input case; it should exit nonzero at the environment assertion:

```bash
ansible-playbook labs/lab03/playbook.yml -e course_environment=production
```

The supported input contract is development or staging. Inspect the existing JSON to confirm the rejected candidate did not replace it.

## Explain

Extra vars override the course environment for that run. A registered result belongs to a task execution on a host; it does not alter the input declaration. An assertion communicates the supported interface early.

Record your predicted result, actual recap, observed artifact, and one corrected assumption. An expected-failure experiment should be recorded as a successful test of a rejected input, not hidden with `ignore_errors`.

## Stretch

Add a `course_owner` string input, validate that it is nonempty, and include it in the JSON.

## Bash alternative

Run [the Bash implementation](alternative.sh) with Bash 3.2+ and standard Unix utilities. It does not require Ansible, Python, jq, or a virtual environment. Follow the [shared Bash guide](../../notes/bash_alternatives.md) for input mappings, change reporting, and boundaries. Its output is separate from the Ansible track.

```bash
bash labs/lab03/alternative.sh
COURSE_ENVIRONMENT=staging bash labs/lab03/alternative.sh
COURSE_ENVIRONMENT=staging bash labs/lab03/alternative.sh
```

Inspect `.sandbox/bash/lab03/variables.json`. Environment variables replace the Ansible input interface; they are text, and there is no Ansible precedence engine. `COURSE_LAST_CHANGED` explicitly records the most recent managed-file result. Try `COURSE_ENVIRONMENT=production` and confirm the existing file survives rejection.

A stable repeat reports `SUMMARY changed=0 check=false`. `--check` predicts this script’s supported changes without writing them; it is an explicitly implemented preview, not Ansible check mode. Adapt this lab’s prediction and drift experiment to the Bash artifact before comparing both implementations.

## Next

[Previous lab](../lab02/README.md) · [Next lab](../lab04/README.md) · [Notes index](../../notes/README.md)

Generated artifacts remain inside `.sandbox/`. To reset all course output, use the documented [cleanup command](../../README.md#reset) after saving anything you need.
