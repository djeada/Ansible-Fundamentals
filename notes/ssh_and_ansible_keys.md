# SSH and keys for a disposable managed host

The core labs use a local connection. This note explains the additional connection work required for an SSH-based VM exercise; none of these commands is needed for the local course.

SSH authentication proves which account can connect. Host-key verification helps prove which server you reached. Ansible privilege escalation determines what that account can do after connecting. Treat these as separate decisions.

## Create a dedicated key

On the controller, choose a new filename and a passphrase. Do not overwrite an existing key.

```bash
ssh-keygen -t ed25519 -C ansible-course -f ~/.ssh/ansible_course
ssh-add ~/.ssh/ansible_course
ssh-copy-id -i ~/.ssh/ansible_course.pub automation@YOUR_VM_ADDRESS
ssh -i ~/.ssh/ansible_course automation@YOUR_VM_ADDRESS
```

Use a key type compatible with your environment's policy; some environments require an alternative to Ed25519. `ssh-add` requires a running SSH agent. Only the `.pub` file is installed on the VM. The private key stays on the controller and is never committed to Git.

Verify the VM's host-key fingerprint through a trusted channel before accepting it. `ssh-keyscan` can collect a presented key, but it does not independently authenticate that key. Keep host-key checking enabled.

## Configure a separate inventory

```yaml
---
all:
  children:
    course_vm:
      hosts:
        vm01:
          ansible_host: YOUR_VM_ADDRESS
          ansible_user: automation
          ansible_ssh_private_key_file: ~/.ssh/ansible_course
```

Save it outside the course inventory, for example as `.sandbox/vm-hosts.yml` after creating that directory. Ansible uses the SSH agent when available; a private-key filename is an option, not a requirement to duplicate keys.

```bash
ansible course_vm -i .sandbox/vm-hosts.yml --list-hosts
ansible course_vm -i .sandbox/vm-hosts.yml -m ansible.builtin.ping
```

The VM needs a suitable Python interpreter for ordinary POSIX Python modules. If automatic discovery chooses incorrectly, explicitly set `ansible_python_interpreter` to the VM's Python path. That path can differ from the controller's virtual environment.

## Add privileges only when required

First prove an unprivileged read-only connection. Then test a narrowly scoped task with `become: true` if the VM account is authorized. `--ask-become-pass` requests the escalation password; `--ask-pass` requests the connection password. These are different credentials. Prefer agent-managed keys over storing a connection password in inventory.

Do not copy this course's `ansible_playbook_python` setting to arbitrary SSH targets: it names the controller interpreter, which may not exist remotely.

## Diagnose the layer that failed

| Symptom | First check |
|---|---|
| Name resolution or connection timeout | Address, route, port, VM status, firewall |
| Host-key mismatch | Verify the VM identity; investigate before replacing a known key |
| `Permission denied (publickey)` | SSH account, selected key, agent, authorized key and permissions |
| Python module cannot execute | Target Python path and supported Python version |
| Sudo/escalation failure | Become settings, account policy, escalation credential |

Increase verbosity only as needed and inspect logs before sharing them; connection output can reveal infrastructure details. Avoid disabling host-key checking as a debugging shortcut.

<details><summary>Self-check: should the VM receive the private key so it can authenticate Ansible?</summary>

No. The controller proves possession of its private key. The VM uses the corresponding authorized public key. Copying private keys increases exposure and is unnecessary for this connection.

</details>

Reference: [Connection details](https://docs.ansible.com/projects/ansible/latest/inventory_guide/connection_details.html).
