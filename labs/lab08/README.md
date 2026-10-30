# Lab 08 · A role with a small interface

Reuse the training_site role and distinguish its defaults, tasks, and template.

## Before you run

Complete lab 07. Read [users, privileges, and roles](../../notes/users_and_roles.md). Run commands from the repository root with `.venv` active. Open [the reference playbook](playbook.yml) after making your prediction.

## Predict

Where does the site title come from? Does using a role change the operating-system user?

## Run

```bash
ansible-playbook labs/lab08/playbook.yml
cat .sandbox/lab08/index.html
ansible-playbook labs/lab08/playbook.yml
ansible-playbook labs/lab08/playbook.yml -e '{"training_site_title": "My revised learning page"}'
```

## Observe

The HTML title and heading reflect the role input. The default run uses the role parameter in this play. An extra variable can override it. The generated file stays under `.sandbox/lab08/`.

## Experiment

Pass an empty title as typed JSON. The role input assertion should fail. Then pass a title containing `<em>hello</em>` and inspect the output: the value should be escaped as text rather than become markup.

## Explain

An Ansible role is reusable content. Its prefixed defaults form a public interface; role parameters and extra vars can override defaults. Task tags select execution and do not pin role code versions.

Record your predicted result, actual recap, observed artifact, and one corrected assumption. An expected-failure experiment should be recorded as a successful test of a rejected input, not hidden with `ignore_errors`.

## Stretch

Add a documented input to the role and use it from both this lab and project 01.

## Next

[Previous lab](../lab07/README.md) · [Next lab](../lab09/README.md) · [Notes index](../../notes/README.md)

Generated artifacts remain inside `.sandbox/`. To reset all course output, use the documented [cleanup command](../../README.md#reset) after saving anything you need.
