# Notes index

Read the concepts in order or follow a question to a worked example. Commands assume an activated virtual environment and the repository root as your working directory.

| Question | Notes | Runnable companion |
|---|---|---|
| What does Ansible actually do? | [Introduction](intro.md) | [Lab 01](../labs/lab01/README.md) |
| How are hosts selected? | [Inventory and targeting](inventory.md) | [Lab 01](../labs/lab01/README.md) |
| When is an ad hoc command useful? | [Ad hoc commands](ad_hoc_commands.md) | [Lab 02](../labs/lab02/README.md) |
| How does a playbook execute? | [Playbooks](playbooks.md) | [Lab 02](../labs/lab02/README.md) |
| Where do values come from? | [Variables and facts](variables_and_facts.md) | [Labs 03–05](../labs/lab03/README.md) |
| How do I render safe configuration? | [Templates](templates.md) | [Lab 06](../labs/lab06/README.md) |
| When should something restart? | [Handlers](handlers.md) | [Lab 07](../labs/lab07/README.md) |
| Is a role a user permission? | [Users, privileges, and roles](users_and_roles.md) | [Lab 08](../labs/lab08/README.md) |
| How do remote connections work? | [SSH and keys](ssh_and_ansible_keys.md) | Optional disposable VM extension |
| How do I handle credentials? | [Vault](vault.md) | [Lab 09](../labs/lab09/README.md) |
| What happens after failure? | [Error handling](error_handling.md) | [Lab 10](../labs/lab10/README.md) |
| How do I limit rollout scope? | [Orchestration](orchestration.md) | [Lab 11](../labs/lab11/README.md) |
| How do I prove it works? | [Testing](testing.md) | [Lab 12](../labs/lab12/README.md) |
| How do I diagnose a failure? | [Troubleshooting](troubleshooting.md) | [Challenges](../exercises/README.md) |
| How does the same lesson work in Bash? | [Bash alternatives](bash_alternatives.md) | All twelve labs |
| What does a term mean? | [Terminology](terminology.md) | [Flashcards](../flashcards/intro.md) |
| What command do I need? | [Command reference](cheat_sheet.md) | All labs |

Examples labeled **task fragment** belong inside a play's `tasks:` list. Examples involving `/etc`, packages, users, or services require an appropriate disposable managed system; the course's local playbooks do not perform those operations.
