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

## Bash alternative

Run [the Bash implementation](alternative.sh) with Bash 3.2+ and standard Unix utilities. It does not require Ansible, Python, jq, or a virtual environment. Follow the [shared Bash guide](../../notes/bash_alternatives.md) for input mappings, change reporting, and boundaries. Its output is separate from the Ansible track.

```bash
bash labs/lab09/alternative.sh
bash labs/lab09/alternative.sh --prompt
# Enter a dummy learning token at the hidden prompt.
# For a pipeline using public practice data only:
printf '%s\n' 'practice-token' | bash labs/lab09/alternative.sh --token-stdin
```

Inspect the permissions of `.sandbox/bash/lab09/token.txt` without printing the value: its directory is mode 0700 and the file is mode 0600. The script disables xtrace before reading a single-line token, suppresses its value in normal output, and supports hidden terminal or standard-input entry. The committed default is a dummy value. **This alternative does not encrypt at rest.** Bash builtins do not replace Vault; use the Ansible Vault exercise or a separate established secret tool when encrypted storage is required. Do not place real tokens in command arguments, environment examples, or shell history.

A stable repeat reports `SUMMARY changed=0 check=false`. `--check` predicts this script’s supported changes without writing them; it is an explicitly implemented preview, not Ansible check mode. Adapt this lab’s prediction and drift experiment to the Bash artifact before comparing both implementations.

## Next

[Previous lab](../lab08/README.md) · [Next lab](../lab10/README.md) · [Notes index](../../notes/README.md)

Generated artifacts remain inside `.sandbox/`. To reset all course output, use the documented [cleanup command](../../README.md#reset) after saving anything you need.
