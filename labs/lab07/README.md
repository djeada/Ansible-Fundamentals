# Lab 07 · Handlers and deliberate reloads

Send a notification only after a relevant change and observe an explicit handler flush.

## Before you run

Complete lab 06. Read [handlers](../../notes/handlers.md). Run commands from the repository root with `.venv` active. Open [the reference playbook](playbook.yml) after making your prediction.

## Predict

Does the handler run after an unchanged copy? What if two changed tasks notify the same handler?

## Run

```bash
ansible-playbook labs/lab07/playbook.yml
cat .sandbox/lab07/reload.txt
ansible-playbook labs/lab07/playbook.yml
ansible-playbook labs/lab07/playbook.yml -e '{"course_message": "new configuration"}'
```

## Observe

The first changed configuration triggers a `RUNNING HANDLER` section and writes the receipt. The unchanged repeat does not run that handler. A new message updates both configuration and receipt. No real service is restarted.

## Experiment

Delete only `.sandbox/lab07/reload.txt`, then repeat the same message input. The configuration is unchanged, so the handler is not notified and the receipt remains absent. Change the message to trigger it again.

## Explain

A handler is an event response, not a substitute for continuously maintaining every desired resource. For a real service, maintain started/enabled state with a normal task and use a handler for a configuration-triggered reload.

Record your predicted result, actual recap, observed artifact, and one corrected assumption. An expected-failure experiment should be recorded as a successful test of a rejected input, not hidden with `ignore_errors`.

## Stretch

Add two configuration tasks notifying the same handler and observe how many times it runs before one flush.

## Next

[Previous lab](../lab06/README.md) · [Next lab](../lab08/README.md) · [Notes index](../../notes/README.md)

Generated artifacts remain inside `.sandbox/`. To reset all course output, use the documented [cleanup command](../../README.md#reset) after saving anything you need.
