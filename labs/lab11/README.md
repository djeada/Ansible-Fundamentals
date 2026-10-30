# Lab 11 · Two-host batching and delegation

Observe serial execution and keep per-host artifacts separate even when aliases share one filesystem.

## Before you run

Complete lab 10. Read [orchestration](../../notes/orchestration.md). Run commands from the repository root with `.venv` active. Open [the reference playbook](playbook.yml) after making your prediction.

## Predict

How many physical machines are involved? Why would both aliases writing one shared path be a race?

## Run

```bash
ansible-inventory -i inventories/simulated/hosts.yml --graph
ansible-playbook -i inventories/simulated/hosts.yml labs/lab11/playbook.yml
cat .sandbox/lab11/node_a/release.txt
cat .sandbox/lab11/node_b/release.txt
ansible-playbook -i inventories/simulated/hosts.yml labs/lab11/playbook.yml
```

## Observe

Both aliases record `release=v1` under their own directories. The play runs one host per batch. The delegated debug task reports the current batch while retaining the original inventory host identity.

## Experiment

Repeat with `--limit node_a` and a new typed release value. Only node A should change. Then run without the limit to converge both. In a disposable edit, add a `run_once` debug task and count executions with `serial: 1`.

## Explain

`run_once` is once per current serial batch. Delegation changes execution location and does not independently serialize shared writes. This simulation teaches ordering, not SSH reachability, service availability, or network isolation.

Record your predicted result, actual recap, observed artifact, and one corrected assumption. An expected-failure experiment should be recorded as a successful test of a rejected input, not hidden with `ignore_errors`.

## Stretch

Describe a real rolling deployment with drain, deploy, bounded health probe, and rejoin steps before attempting project 02.

## Next

[Previous lab](../lab10/README.md) · [Next lab](../lab12/README.md) · [Notes index](../../notes/README.md)

Generated artifacts remain inside `.sandbox/`. To reset all course output, use the documented [cleanup command](../../README.md#reset) after saving anything you need.
