# Inventory and targeting

An inventory maps logical names to managed systems. `inventory_hostname` is the name in inventory; `ansible_host` is the address used to connect when it differs. A host may belong to several groups, and group membership can carry shared variables.

## Inspect before executing

```bash
ansible-inventory --graph
ansible-inventory --host localhost
ansible sandbox --list-hosts
ansible-playbook labs/lab02/playbook.yml --list-hosts
```

The supplied local inventory has one host in the `sandbox` group. Its `ansible_python_interpreter` follows `ansible_playbook_python`, keeping the local module interpreter aligned with your activated environment. `training_root` resolves to the repository's `.sandbox/` directory.

A separate [simulated inventory](../inventories/simulated/hosts.yml) contains `node_a` and `node_b`. Both use a local connection. They are useful for observing per-host variables, batches, and result reporting, but they are not separate machines.

```bash
ansible-inventory -i inventories/simulated/hosts.yml --graph
ansible sandbox -i inventories/simulated/hosts.yml --list-hosts --limit node_a
```

## Host patterns

| Pattern | Selection |
|---|---|
| `all` | Every host in the active inventory |
| `sandbox` | Hosts in this course's group |
| `node_a` | One inventory alias |
| `web:database` | Union of groups |
| `web:&staging` | Hosts in both groups |
| `web:!maintenance` | Web hosts excluding the maintenance group |

Quote patterns containing shell metacharacters. `--limit` intersects with the hosts already selected by a play; it does not add hosts outside that selection.

## Variables next to inventory

For a larger separate exercise, use `inventories/development/hosts.yml` with sibling `group_vars/all.yml`, `group_vars/web.yml`, and `host_vars/web01.yml`. This keeps environment data near host membership while roles stay reusable. Avoid defining the same operational input in many locations.

Illustrative remote inventory, for a disposable VM only:

```yaml
---
all:
  children:
    web:
      hosts:
        web01:
          ansible_host: 192.0.2.10
          ansible_user: automation
```

`192.0.2.10` is a documentation address; replace it with your VM's address in your own inventory. Do not put passwords into inventory. Read [SSH and keys](ssh_and_ansible_keys.md) first. The course playbooks intentionally reject this remote connection.

## Common mistakes

- Running from another directory can select another configuration file or no course inventory. Check `ansible --version` for the config path.
- Defining a group and host with the same name makes output harder to interpret.
- Multiple group memberships can introduce variable conflicts. Inspect the host's effective inventory variables before debugging a role.
- `ansible-inventory --list` can expose credentials if you put them in variables. Treat its output as potentially sensitive.
- A comma in `-i 'localhost,'` creates an inline host list; it does not load the course's variables. Use the supplied inventory for course playbooks.

<details><summary>Self-check: can --limit node_b make a play targeting node_a run on node_b?</summary>

No. The intersection is empty, so no host matches. Fix the play's target or the limit; do not assume a successful empty run configured anything.

</details>

Reference: [Inventory guide](https://docs.ansible.com/projects/ansible/latest/inventory_guide/intro_inventory.html), [patterns](https://docs.ansible.com/projects/ansible/latest/inventory_guide/intro_patterns.html).
