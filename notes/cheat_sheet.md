# Command reference

Run from the repository root with `.venv` active. The local inventory is the default; specify the simulated inventory for two-host exercises.

| Goal | Command |
|---|---|
| See installation and config | `ansible --version` |
| Inspect non-default configuration | `ansible-config dump --only-changed` |
| View inventory groups | `ansible-inventory --graph` |
| View a host's inventory data | `ansible-inventory --host localhost` |
| Confirm selected hosts | `ansible sandbox --list-hosts` |
| Test module execution | `ansible sandbox -m ansible.builtin.ping` |
| Read module documentation | `ansible-doc ansible.builtin.template` |
| Check playbook syntax | `ansible-playbook labs/lab06/playbook.yml --syntax-check` |
| List tasks | `ansible-playbook labs/lab12/playbook.yml --list-tasks` |
| Run with diff | `ansible-playbook labs/lab02/playbook.yml --diff` |
| Predict supported changes | `ansible-playbook labs/lab02/playbook.yml --check --diff` |
| Pass a typed integer | `ansible-playbook labs/lab06/playbook.yml -e '{"course_port": 9090}'` |
| Verify without repair | `ansible-playbook labs/lab12/playbook.yml --tags verify` |
| Run simulated hosts | `ansible-playbook -i inventories/simulated/hosts.yml labs/lab11/playbook.yml` |
| Limit simulated scope | Add `--limit node_a` to the previous command |
| Create encrypted local vars | `ansible-vault create .sandbox/vault.local.yml` |
| Pass encrypted local vars | `ansible-playbook labs/lab09/playbook.yml -e @.sandbox/vault.local.yml --ask-vault-pass` |
| Run a Bash alternative | `bash labs/lab02/alternative.sh` |
| Preview Bash changes | `bash labs/lab02/alternative.sh --check` |
| Verify Bash behavior | `python3 scripts/verify_bash.py` |
| Remove Bash output only | `bash scripts/bash/cleanup.sh` |
| Run content validation | `python scripts/check_content.py` |
| Lint YAML | `yamllint -s .` |
| Validate all playbook syntax | `python scripts/verify.py --syntax-only` |
| Run the behavior suite | `python scripts/verify.py` |
| Remove all generated course output | `ansible-playbook playbooks/cleanup.yml` |

`--check` is not a universal safety boundary; inspect module support and tasks that opt out. Diff and inventory output may reveal secrets. See [testing](testing.md) and [Vault](vault.md) for the relevant limits.
