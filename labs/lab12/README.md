# Lab 12 · Verification without repair

Separate configuration from observation, detect drift with tags, and run the repository checks.

## Before you run

Complete lab 11. Read [testing](../../notes/testing.md). Run commands from the repository root with `.venv` active. Open [the reference playbook](playbook.yml) after making your prediction.

## Predict

Can a successful copy prove the application contract? Will a verify-only run fix a corrupt file?

## Run

```bash
ansible-playbook labs/lab12/playbook.yml
ansible-playbook labs/lab12/playbook.yml --tags verify
ansible-playbook labs/lab12/playbook.yml --check --diff
python scripts/check_content.py
python scripts/verify.py --syntax-only
```

## Observe

The deployed JSON declares version v1 and a boolean healthy value. Verification reads actual bytes and checks both fields. After a real converge, warm check mode predicts no changes; verification depending on newly deployed bytes is skipped in check mode.

## Experiment

Edit `.sandbox/lab12/release.json` to set `version` to `v9`, leaving valid JSON. Run with `--tags verify`: it must exit nonzero without repairing the file. Then run normally to repair it. Also try `-e course_expected_version=v9` to make the assertion fail without changing the declared release.

## Explain

Syntax, convergence, idempotence, and correctness are different claims. Verification should inspect observable state rather than merely trust the mutation result. The full suite runs in a temporary copy so experiments in your working sandbox are preserved.

Record your predicted result, actual recap, observed artifact, and one corrected assumption. An expected-failure experiment should be recorded as a successful test of a rejected input, not hidden with `ignore_errors`.

## Stretch

Complete the three projects, then run `python scripts/verify.py` and explain one failure-path assertion from the verifier.

## Next

[Previous lab](../lab11/README.md) · [Project 01](../../projects/01-learning-site/README.md) · [Notes index](../../notes/README.md)

Generated artifacts remain inside `.sandbox/`. To reset all course output, use the documented [cleanup command](../../README.md#reset) after saving anything you need.
