# Lab 05 · Structured loops and per-item selection

Loop over dictionaries, give readable labels, and select enabled items with a boolean field.

## Before you run

Complete lab 04. Review lists and dictionaries in the [variables notes](../../notes/variables_and_facts.md). Run commands from the repository root with `.venv` active. Open [the reference playbook](playbook.yml) after making your prediction.

## Predict

Will the disabled worker have a directory? Will it have a configuration file?

## Run

```bash
ansible-playbook labs/lab05/playbook.yml
cat .sandbox/lab05/web/service.conf
ansible-playbook labs/lab05/playbook.yml
```

## Observe

Both web and worker directories exist. Only web has `service.conf`, containing `port=8080`. The copy iteration for worker is skipped because its `enabled` field is false.

## Experiment

Edit the play's worker entry to `enabled: true`, run it, then set it back to false and run again. Inspect the worker directory: its old configuration remains. The conditional prevents future writes; it does not remove prior state.

## Explain

Absence is also desired state that needs an explicit task. If disabled means removed, add an `ansible.builtin.file` task with `state: absent` and a matching condition. A loop result has per-item records under `results`.

Record your predicted result, actual recap, observed artifact, and one corrected assumption. An expected-failure experiment should be recorded as a successful test of a rejected input, not hidden with `ignore_errors`.

## Stretch

Implement removal for disabled configurations and verify a true → false transition without deleting the whole sandbox.

## Next

[Previous lab](../lab04/README.md) · [Next lab](../lab06/README.md) · [Notes index](../../notes/README.md)

Generated artifacts remain inside `.sandbox/`. To reset all course output, use the documented [cleanup command](../../README.md#reset) after saving anything you need.
