# Projects: design, prove, and recover

Work from the brief before opening each reference implementation. Each project combines earlier skills and adds an operational contract you can test. Use the [assessment rubric](../CURRICULUM.md#project-assessment-rubric) and submit a short evidence log rather than only a green screenshot.

| Project | Prerequisites | Main contract |
|---|---|---|
| [01 · Learning site](01-learning-site/README.md) | Labs 01–08 | Validated environment inputs produce stable, escaped HTML |
| [02 · Rolling release](02-rolling-release/README.md) | Labs 01–12 | A failed host is restored and later batches stop |
| [03 · Backup and restore](03-backup-restore/README.md) | Labs 01–12 | Restore verifies the stored snapshot checksum before writing |

All references use a local connection and files in `.sandbox/`. The optional VM extensions require a separate inventory and explicit review of connection, privileges, and service dependencies. Read [SSH notes](../notes/ssh_and_ansible_keys.md) before attempting them.
