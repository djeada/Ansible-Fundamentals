# Vault and the secret lifecycle

Ansible Vault encrypts data at rest. At runtime, Ansible decrypts it so a task can use it. Vault does not automatically protect a plaintext destination, debug output, command arguments, editor swap files, controller memory, or an external service receiving the secret.

## A complete local exercise

Run [lab 09](../labs/lab09/README.md) for the exact steps. Its committed input is explicitly a dummy value. You then create an encrypted variable file locally and pass it as extra vars:

```bash
mkdir -p .sandbox
ansible-vault create .sandbox/vault.local.yml
# In the editor, enter a dummy learning value:
# course_api_token: practice-token
ansible-playbook labs/lab09/playbook.yml -e @.sandbox/vault.local.yml --ask-vault-pass
```

The editor receives plaintext while you edit. Use a dummy token, configure your editor sensibly, and keep temporary files private. Never commit the Vault password alongside an encrypted file.

## Three different controls

| Control | What it protects | Limit |
|---|---|---|
| Vault encryption | Stored encrypted input | Data must be decrypted to use it |
| `no_log: true` | Normal task result output | Does not protect separately logged or manually debugged values |
| `diff: false` | Before/after file differences | Does not encrypt the destination |
| Mode `'0600'` and private directory | Target file access by other ordinary users | Does not prevent access by the owner or privileged accounts |

Lab 09 applies all relevant controls to its token-writing task. Inspect the mode without printing the token. Avoid `debug: var=...` for a secret even when other tasks use `no_log`.

## Operations

```bash
ansible-vault view .sandbox/vault.local.yml
ansible-vault edit .sandbox/vault.local.yml
ansible-vault rekey .sandbox/vault.local.yml
```

`view` deliberately displays decrypted content in your terminal. Rekeying changes encryption credentials; it does not rotate the underlying service credential. Those are separate operations.

For multiple environments, Vault IDs can label distinct password sources. A label helps select a credential source but is not a permission boundary. In CI, use a protected secret provider and a password-client mechanism appropriate for your platform; do not put a password in a committed script or an echoed shell command.

## A useful review question

For each secret, trace where it is created, encrypted, decrypted, rendered, consumed, logged, rotated, and deleted. Decide whether your automation should retrieve a short-lived credential at runtime rather than keep a long-lived encrypted value in Git.

<details><summary>Self-check: does --check --diff make a secret-handling play safe to share?</summary>

No. Diff output can disclose configuration values, and a task can explicitly opt out of check mode. Inspect the playbook and use output controls. Avoid sharing sensitive logs in the first place.

</details>

Reference: [Vault guide](https://docs.ansible.com/projects/ansible/latest/vault_guide/index.html).
