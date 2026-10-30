# Lab 10 · Blocks, rescue, and honest recovery

Observe a deliberate validation failure, successful rescue, and a later valid promotion.

## Before you run

Complete lab 09. Read [error handling](../../notes/error_handling.md). Run commands from the repository root with `.venv` active. Open [the reference playbook](playbook.yml) after making your prediction.

## Predict

Will the default invalid candidate overwrite the live configuration? Does rescue automatically undo writes?

## Run

```bash
ansible-playbook labs/lab10/playbook.yml
cat .sandbox/lab10/live.conf
ansible-playbook labs/lab10/playbook.yml -e '{"course_candidate_valid": true}'
cat .sandbox/lab10/live.conf
```

## Observe

On a fresh sandbox, the default run seeds version 1, rejects the candidate, and records a rescued task while the run succeeds. The valid candidate promotes version 2. Repeating the default afterward preserves the current live version; seeding uses `force: false`.

## Experiment

Move a write before the deliberately failed assertion in a disposable copy of the block. Predict and inspect the surviving file. Restore the reference afterward. Why did a successful rescue message not reverse that earlier write?

## Explain

The reference protects the file by validating before promotion. Rescue is control flow, not a transaction. Project 02 shows an explicit snapshot restoration and a final failure to preserve the deployment outcome.

Record your predicted result, actual recap, observed artifact, and one corrected assumption. An expected-failure experiment should be recorded as a successful test of a rejected input, not hidden with `ignore_errors`.

## Stretch

Add an observable recovery result and a test asserting both the final file state and the intended exit status.

## Bash alternative

Run [the Bash implementation](alternative.sh) with Bash 3.2+ and standard Unix utilities. It does not require Ansible, Python, jq, or a virtual environment. Follow the [shared Bash guide](../../notes/bash_alternatives.md) for input mappings, change reporting, and boundaries. Its output is separate from the Ansible track.

```bash
bash labs/lab10/alternative.sh
COURSE_CANDIDATE_VALID=true bash labs/lab10/alternative.sh
bash labs/lab10/alternative.sh
```

Inspect `.sandbox/bash/lab10/live.conf`. The initial version is seeded only when absent. Explicit `if`/`else` branches either promote version 2 or report a handled rejection before promotion. The default repeat retains an existing version 2. `set -e` is not an Ansible rescue block or transaction; the recovery policy must be written explicitly. A handled rejection exits successfully here, matching this lab’s Ansible reference.

A stable repeat reports `SUMMARY changed=0 check=false`. `--check` predicts this script’s supported changes without writing them; it is an explicitly implemented preview, not Ansible check mode. Adapt this lab’s prediction and drift experiment to the Bash artifact before comparing both implementations.

## Next

[Previous lab](../lab09/README.md) · [Next lab](../lab11/README.md) · [Notes index](../../notes/README.md)

Generated artifacts remain inside `.sandbox/`. To reset all course output, use the documented [cleanup command](../../README.md#reset) after saving anything you need.
