# Ad-hoc Commands

Ansible ad-hoc commands are single, standalone tasks executed directly from the command line without needing to create a playbook. These commands are ideal for quick, one-off tasks and troubleshooting activities across multiple hosts.

## Basic Structure of Ad-hoc Commands

The general syntax for Ansible ad-hoc commands is:

```bash
ansible <host-pattern> -m <module_name> -a "module arguments"
```

- `host-pattern`: Targeted hosts or groups from inventory.
- `-m`: Specifies the module to run.
- `-a`: Passes arguments to the module.

## Example: Checking Connectivity

Use the `ping` module to verify host connectivity:

```bash
ansible all -m ping
```

Example output:
```
host1 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

Interpretation:
- Successfully connected and received a response from `host1`.

## File Management with Ad-hoc Commands

Use the `copy` module to manage files:

```bash
ansible webservers -m copy -a "src=/path/to/file dest=/etc/myfile mode=0644"
```

Example output:
```
webserver1 | CHANGED => {
    "changed": true,
    "dest": "/etc/myfile",
    "src": "/path/to/file"
}
```

Interpretation:
- File successfully copied to target hosts.

## Managing Packages

The `apt` (or `yum`) module installs, updates, or removes packages:

```bash
ansible database -m apt -a "name=mysql-server state=present"
```

Example output:
```
db01 | CHANGED => {
    "changed": true,
    "name": "mysql-server",
    "state": "present"
}
```

Interpretation:
- MySQL successfully installed or updated on target hosts.

## Service Management

Use the `service` module to control system services:

```bash
ansible all -m service -a "name=nginx state=started enabled=yes"
```

Example output:
```
host1 | CHANGED => {
    "changed": true,
    "name": "nginx",
    "state": "started",
    "enabled": true
}
```

Interpretation:
- Ensures nginx service is running and enabled on system boot.

## Using Conditional Execution

Ad-hoc commands can execute conditionally by using the `-l` (limit) or inventory patterns:

```bash
ansible webservers[0] -m shell -a "uptime"
```

Example output:
```
webserver1 | CHANGED | rc=0 >>
 15:35:01 up 3 days,  2:18,  1 user,  load average: 0.00, 0.01, 0.05
```

Interpretation:
- Command executed only on the first host in the `webservers` group.

## Using Tags in Ad-hoc Commands

While tags are generally used in playbooks, you can emulate selective execution by targeting specific hosts or groups explicitly:

```bash
ansible webservers -m command -a "ls -l /var/www"
```

Example output:
```
webserver1 | CHANGED | rc=0 >>
total 4
drwxr-xr-x 2 root root 4096 Mar 15 12:00 html
```

Interpretation:
- Lists content of `/var/www` directory on targeted webservers.

## Advanced Ad-hoc Command Example

Using advanced options such as privilege escalation (`become`):

```bash
ansible all -b -m apt -a "update_cache=yes"
```

Example output:
```
host1 | CHANGED => {
    "changed": true
}
```

Interpretation:
- System package cache updated on all target hosts using elevated privileges.

## Visual Diagram of Ad-hoc Command Execution Flow

```
+---------------------------+
| Command-line (Ad-hoc Cmd) |
+---------------------------+
             |
             v
+---------------------------+
| Ansible Module Execution  |
+---------------------------+
             |
             v
+---------------------------+
|      Target Host(s)       |
+---------------------------+
```

- Command-line ad-hoc instruction invokes specific modules.
- Modules execute on targeted hosts instantly.
