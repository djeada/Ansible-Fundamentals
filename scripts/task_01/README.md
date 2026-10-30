# Retired container/MySQL experiment

The former example combined an Alpine SSH container, a MariaDB client package, a service-start task, and an unavailable `mysql_secure_installation` action. It could not install and operate the database it claimed to manage. It also embedded learning passwords and referred to an unprovided key file.

The incomplete Dockerfile and playbook have been removed. Use the supported learning path instead:

- [Lab 01](../../labs/lab01/README.md) for a working controller and connection exercise.
- [SSH notes](../../notes/ssh_and_ansible_keys.md) for an optional disposable VM connection.
- [Project 03](../../projects/03-backup-restore/README.md) for a runnable backup/restore contract and a clearly scoped database extension.

A future database project should identify its target OS, install a real server, use an explicitly declared collection/module dependency, protect credentials, and verify an isolated restore. It should not be presented as runnable until those requirements are tested.
