# Lab 09 · Vault and private runtime files

Use a dummy token to distinguish encrypted input, suppressed output, and a plaintext runtime destination.

## Before you run

Complete lab 08. Read [Vault](../../notes/vault.md). Use learning values only. Run commands from the repository root with `.venv` active. Open [the reference playbook](playbook.yml) after making your prediction.

## Predict

Which file will be encrypted? Which file must contain plaintext for its consumer? Will diff show the token?

## Run

```bash
ansible-playbook labs/lab09/playbook.yml --diff
mkdir -p .sandbox
ansible-vault create .sandbox/vault.local.yml
# In the editor, enter: course_api_token: practice-token
ansible-playbook labs/lab09/playbook.yml -e @.sandbox/vault.local.yml --ask-vault-pass
ansible-playbook labs/lab09/playbook.yml -e @.sandbox/vault.local.yml --ask-vault-pass
```

## Observe

The committed example is a public dummy token. The created variable file begins with an Ansible Vault header when viewed as raw text. The token-writing task hides its result and diff; `.sandbox/lab09/token.txt` is a private mode-0600 plaintext file.

## Experiment

Run once with the wrong Vault password and observe failure to decrypt before secret use. Correct it and repeat. Use your file inspector or `stat` to check permissions without printing the token. Explain why `no_log` on this task would not protect a separate debug task.

## Explain

Vault protects input at rest. `no_log` and `diff: false` control normal output. Directory/file permissions restrict runtime access. None of these automatically rotates a service credential. Never commit a Vault password.

Record your predicted result, actual recap, observed artifact, and one corrected assumption. An expected-failure experiment should be recorded as a successful test of a rejected input, not hidden with `ignore_errors`.

## Stretch

Use `ansible-vault rekey` on the dummy variable file and explain how that differs from changing the token value.

## Next

[Previous lab](../lab08/README.md) · [Next lab](../lab10/README.md) · [Notes index](../../notes/README.md)

Generated artifacts remain inside `.sandbox/`. To reset all course output, use the documented [cleanup command](../../README.md#reset) after saving anything you need.
