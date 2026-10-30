# Lab 04 · Facts and boolean conditions

Collect selected host facts and use a boolean condition to choose behavior.

## Before you run

Complete lab 03. Read the facts and type sections in [variables](../../notes/variables_and_facts.md). Run commands from the repository root with `.venv` active. Open [the reference playbook](playbook.yml) after making your prediction.

## Predict

Why can a fact-based condition fail if fact gathering is disabled? Should a stable file include the current time?

## Run

```bash
ansible-playbook labs/lab04/playbook.yml
cat .sandbox/lab04/facts.json
ansible-playbook labs/lab04/playbook.yml
```

## Observe

The JSON records system and architecture. On Linux the explanatory task runs; on other systems it is skipped. The repeat should not rewrite the stable facts file merely because time passed.

## Experiment

In a disposable edit of the playbook, set `gather_facts: false` and run again. Identify the missing prerequisite, then restore `true`. Do not fix the undefined fact with an invented default that pretends to know the operating system.

## Explain

Facts describe the target, and `ansible_facts['system'] == 'Linux'` yields a boolean. Fact collection and inventory inputs answer different questions. Check a fact's availability and freshness before relying on it.

Record your predicted result, actual recap, observed artifact, and one corrected assumption. An expected-failure experiment should be recorded as a successful test of a rejected input, not hidden with `ignore_errors`.

## Stretch

Add one stable fact and one conditional debug task for a platform you can explain.

## Bash alternative

Run [the self-contained Bash implementation](alternative.sh) with Bash 3.2+ and standard Unix utilities. It does not require Ansible, Python, jq, or a virtual environment. Follow the [shared Bash guide](../../notes/bash_alternatives.md) for input mappings, change reporting, and boundaries. Its output is separate from the Ansible track.

```bash
bash labs/lab04/alternative.sh
bash labs/lab04/alternative.sh
```

Inspect `.sandbox/bash/lab04/facts.json`. `uname -s` and `uname -m` provide a small set of local facts, and an `if` selects Linux behavior. This is a local probe, not Ansible fact gathering or a fact cache. Keep volatile timestamps out of the managed output.

A stable repeat reports `SUMMARY changed=0 check=false`. `--check` predicts this script’s supported changes without writing them; it is an explicitly implemented preview, not Ansible check mode. Adapt this lab’s prediction and drift experiment to the Bash artifact before comparing both implementations.

## Next

[Previous lab](../lab03/README.md) · [Next lab](../lab05/README.md) · [Notes index](../../notes/README.md)

Generated artifacts remain inside `.sandbox/`. To reset all course output, use the documented [cleanup command](../../README.md#reset) after saving anything you need.
