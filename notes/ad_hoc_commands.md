# Ad hoc commands

An ad hoc command invokes a module without creating a playbook. It is useful for inspection and small, deliberate operations. Move repeatable workflows into named tasks in version control.

The shape is `ansible PATTERN -m MODULE -a ARGUMENTS`. Inventory and connection settings still apply. Use fully qualified module names so the selected module is unambiguous.

## Read-only inspection

```bash
ansible sandbox --list-hosts
ansible sandbox -m ansible.builtin.ping
ansible sandbox -m ansible.builtin.setup -a 'filter=ansible_system'
ansible sandbox -m ansible.builtin.command -a '{"argv": ["python3", "--version"]}'
ansible-doc ansible.builtin.copy
ansible-doc ansible.builtin.command
```

`command` does not interpret shell pipelines, redirects, or shell expansion. Prefer `argv` for arguments that might contain spaces or external input. The version command is a read-only probe, but an ad hoc `command` invocation normally reports `changed`; output classification is a module contract, not a universal side-effect detector.

`setup` can return considerable machine information. Filter what you need and avoid posting complete fact dumps publicly.

## Observe a file after lab 02

```bash
ansible-playbook labs/lab02/playbook.yml
ansible sandbox -m ansible.builtin.stat -a 'path=.sandbox/lab02/managed.txt'
```

This relative path works because the supplied connection is local and the command is run from the repository root. On an SSH host, a relative target path is relative to that host's execution context. Use absolute managed paths in remote automation.

## Command versus shell

| Module | Use it for | Design responsibility |
|---|---|---|
| `ansible.builtin.command` | A program with explicit arguments | Define change detection and accepted return codes |
| `ansible.builtin.shell` | A necessary shell feature such as a pipeline | Quote inputs, choose the shell, consider pipeline failure behavior |
| A dedicated module | A supported resource such as a file or package | Choose the desired state and validate inputs |

Do not interpolate untrusted text into a shell command. Prefer a module or pass an argument list. `creates` and `removes` can guard a command using filesystem state, but a stale marker may hide drift in the actual resource.

## From an inspection to a repeatable task

```yaml
# Task fragment: classify a read-only command correctly.
- name: Read tool version
  ansible.builtin.command:
    argv: [python3, --version]
  register: tool_version
  changed_when: false
  failed_when: tool_version.rc != 0
```

`changed_when: false` is appropriate here because the command only reads a version. Applying it to a real mutation would hide changes and prevent handlers from being notified.

<details><summary>Self-check: why does command: cat file | grep x fail?</summary>

`command` passes the pipe and following text as literal arguments. Use a suitable module or filter the registered output. Use `shell` only if you actually need shell interpretation and understand its quoting and return-code behavior.

</details>

Continue with [playbooks](playbooks.md) and [lab 02](../labs/lab02/README.md). Reference: [Ad hoc commands](https://docs.ansible.com/projects/ansible/latest/command_guide/intro_adhoc.html).
