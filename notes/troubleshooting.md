# Troubleshooting by execution layer

Start with the first meaningful error, the task name, the selected host, and the phase that failed. Re-running a mutation with more verbosity is not always the best first step.

## A short diagnostic sequence

```bash
pwd
ansible --version
ansible-config dump --only-changed
ansible-inventory --graph
ansible-playbook labs/lab02/playbook.yml --list-hosts
ansible-playbook labs/lab02/playbook.yml --syntax-check
```

Confirm the repository root, virtual environment, configuration path, inventory, and actual target set. Then inspect the failing task's inputs. Use `ansible-doc MODULE` to check parameters and return values for the installed version.

## Symptoms and evidence

| Symptom | Likely layer | Useful next step |
|---|---|---|
| `ansible-playbook` not found | Controller installation | Activate `.venv`; inspect `python -m pip show ansible-core` |
| Unexpected config path | Configuration discovery | Run from the repo root; inspect `ANSIBLE_CONFIG` |
| Config ignored in world-writable directory | Configuration discovery | Use a private checkout or explicitly select a reviewed config |
| No hosts matched | Inventory/pattern/limit | Compare `--graph` and `--list-hosts`; inspect `--limit` |
| `UNREACHABLE` | Connection/authentication | For SSH, first establish an ordinary verified SSH connection |
| Undefined variable | Data scope or spelling | Inspect the precise name and where it should be defined |
| Conditional is not boolean | Expression/type | Use a comparison; pass typed YAML/JSON inputs |
| Module/action not found | Module name/dependency | Check the FQCN and installed collection versions |
| Permission denied writing a file | Target filesystem privilege | Inspect target path and ownership before adding escalation |
| Service manager unavailable | Target environment | Confirm that the target has the expected init system |
| Every repeat reports changes | State contract | Inspect timestamps, unconditional commands, restart tasks, and modes |
| Check mode fails only on an empty target | Missing predicted prerequisite | Compare warm check mode after a real converge |
| Handler did not run | Notification/change/failure path | Check `changed`, handler name, flush timing, and later task failures |
| Restore integrity assertion fails | Snapshot or manifest mismatch | Stop; inspect the selected backup ID and recorded checksum |
| Local RPC/socket error before any task | Controller restrictions | Use a normal environment permitting local sockets/processes or repository CI |

## Debug the smallest relevant value

Use `debug` for non-sensitive values or `type_debug` to inspect their type. Avoid dumping all host variables. A registered loop result is a list under `results`; a skipped result may lack fields from a successful run. A controller lookup reads the controller, not the remote host.

Increase to `-v`, then `-vv`, then `-vvv` only as needed. Inspect output for secrets, addresses, paths, and credentials before sharing it. `no_log` on one task does not sanitize a separate debug task.

## Avoid making the problem disappear

Do not add `ignore_errors`, disable host-key checking, broadly enable `become`, or set `changed_when: false` merely to make output green. State the expected behavior, collect evidence at the failing layer, and make the narrow correction.

`--start-at-task` and selective tags can skip prerequisites. Prefer a complete repeatable run during diagnosis unless you know the skipped state already exists. `--step` can help inspect a controlled local experiment, but it is not a replacement for tests.

## A useful bug report

Include the core and Python versions, config path, inventory shape with sensitive data removed, exact command, smallest failing task, expected state, actual error, and whether the failure happens on a first or repeated run. Never attach a real Vault password or decrypted credential file.

Practice: [debugging challenges](../exercises/README.md).
