# Lab 06 · Validated Jinja templates

Render structured JSON, enforce a typed port input, and validate output before replacement.

## Before you run

Complete lab 05. Read [templates](../../notes/templates.md). Run commands from the repository root with `.venv` active. Open [the reference playbook](playbook.yml) after making your prediction.

## Predict

What is the type of a key=value extra var? How would a message containing a quote affect hand-written JSON?

## Run

```bash
ansible-playbook labs/lab06/playbook.yml
ansible-playbook labs/lab06/playbook.yml -e '{"course_port": 9090, "course_message": "say \"hello\""}'
python -m json.tool .sandbox/lab06/app.json
ansible-playbook labs/lab06/playbook.yml -e '{"course_port": 9090, "course_message": "say \"hello\""}'
```

## Observe

The parser accepts the artifact, the port is a JSON number, and the quoted message remains a valid string. Repeating identical typed inputs reports zero changes.

## Experiment

Try the following invalid input; the assertion should fail before the existing app file is replaced:

```bash
ansible-playbook labs/lab06/playbook.yml -e course_port=9090
```

Then, in a disposable template edit, append an invalid JSON token and run with the default valid input. The `validate` command should reject it. Restore the template and rerun.

## Explain

Input validation proves the port contract; serialization handles escaping; the target-side validator checks the rendered syntax. These are separate checks. The local Python path used here must not be assumed to exist on arbitrary SSH hosts.

Record your predicted result, actual recap, observed artifact, and one corrected assumption. An expected-failure experiment should be recorded as a successful test of a rejected input, not hidden with `ignore_errors`.

## Stretch

Add a list of enabled features using the JSON serializer and independently validate its type.

## Bash alternative

Run [the self-contained Bash implementation](alternative.sh) with Bash 3.2+ and standard Unix utilities. It does not require Ansible, Python, jq, or a virtual environment. Follow the [shared Bash guide](../../notes/bash_alternatives.md) for input mappings, change reporting, and boundaries. Its output is separate from the Ansible track.

```bash
bash labs/lab06/alternative.sh
COURSE_PORT=9090 COURSE_MESSAGE='say "hello"' bash labs/lab06/alternative.sh
COURSE_PORT=9090 COURSE_MESSAGE='say "hello"' bash labs/lab06/alternative.sh --check
```

Inspect `.sandbox/bash/lab06/app.json`. Bash environment inputs are text, so the script accepts only canonical decimal ports from 1025 to 65535 before emitting a JSON number. The serializer in this file escapes JSON strings, including control characters. Try `COURSE_PORT=08080` or `COURSE_PORT=65536`: both must fail before replacement. This is validation of known inputs and a known generated shape; Bash does not include a general JSON parser or Ansible’s target-side `template.validate` operation.

A stable repeat reports `SUMMARY changed=0 check=false`. `--check` predicts this script’s supported changes without writing them; it is an explicitly implemented preview, not Ansible check mode. Adapt this lab’s prediction and drift experiment to the Bash artifact before comparing both implementations.

## Next

[Previous lab](../lab05/README.md) · [Next lab](../lab07/README.md) · [Notes index](../../notes/README.md)

Generated artifacts remain inside `.sandbox/`. To reset all course output, use the documented [cleanup command](../../README.md#reset) after saving anything you need.
