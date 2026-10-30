# Project 03 · Backup, integrity, and restore rehearsal

Build a small backup/restore workflow using fixture JSON data. A backup is useful only when you can select it, verify it, and restore it into a known destination. This project rehearses those behaviors without touching a real database.

## Brief before the reference

Seed a source fixture without overwriting learner edits. Store snapshots under validated identifiers and preserve each snapshot's original checksum manifest. Reusing an identifier for changed source data must fail rather than silently replace the snapshot. Before restore, compare the selected snapshot with its stored manifest, then restore into a separate file and verify the result.

A damaged snapshot must be rejected **before** changing the restore destination. A normal repeat of backup or restore must be stable.

## Back up and restore

```bash
ansible-playbook projects/03-backup-restore/backup.yml
ansible-playbook projects/03-backup-restore/backup.yml
ansible-playbook projects/03-backup-restore/restore.yml
ansible-playbook projects/03-backup-restore/restore.yml
python -m json.tool .sandbox/projects/backup/restored.json
```

Inspect these artifacts:

| Path under `.sandbox/projects/backup/` | Purpose |
|---|---|
| `source.json` | Seeded source, editable for experiments |
| `snapshots/snapshot-001.json` | Immutable-by-policy snapshot bytes |
| `snapshots/snapshot-001.sha256` | Checksum recorded at snapshot creation |
| `restored.json` | Separate rehearsal destination |

“Immutable” here means the playbook uses `force: false` and rejects inconsistency. The local owner can still edit files; this is not a tamper-proof storage system.

## Change the source

Edit a learner name in `.sandbox/projects/backup/source.json`, keeping valid JSON. Re-run backup with the default ID: it should exit nonzero because the existing snapshot does not represent the new source. Select a new ID:

```bash
ansible-playbook projects/03-backup-restore/backup.yml -e course_backup_id=snapshot-002
ansible-playbook projects/03-backup-restore/restore.yml -e course_backup_id=snapshot-002
```

The second snapshot should reflect the edit while the first remains unchanged. The source is seeded with `force: false`, so automation does not erase your changed data before backing it up.

## Corrupt a snapshot

After a successful restore, edit `snapshots/snapshot-002.json` directly without editing its checksum file. Run restore for snapshot-002 again. It must fail the integrity assertion and leave the previous `restored.json` bytes unchanged. The automated verifier checks this exact property.

Restore snapshot-001 to demonstrate that a different intact snapshot remains usable. Preserve the original corrupted snapshot if you want evidence for diagnosis; do not “fix” the checksum to make an unknown backup appear valid.

## Explain the guarantees

The manifest gives a stored reference against which to detect accidental byte changes. It does not establish authenticity if an attacker can replace both data and manifest. The source must remain stable while it is copied; this file-only reference does not provide a concurrent-writer snapshot protocol.

A valid checksum does not establish valid JSON, a consistent database snapshot, compatible application schema, or recoverability of dependent services. Add those checks when the data contract requires them.

Backup and restore check mode are intended for initialized, existing artifacts. Cold check mode cannot manufacture source/snapshot files for later read tasks. Real execution, independent byte comparison, and failure injection remain the primary evidence.

## Extensions

1. Validate JSON and its expected schema before accepting a restore. Keep integrity validation before any destination write.
2. Add a snapshot catalog with creation metadata stored once. Avoid rewriting timestamps on every repeat.
3. Define retention policy that keeps at least one verified restorable snapshot. Test selection before adding deletion behavior.
4. For a PostgreSQL extension, choose a consistent `pg_dump`/`pg_restore` workflow, encrypt stored backups, define credential handling, and restore into an isolated test database. Verify schema and application queries, not only file size or checksum.

Submit evidence of a stable repeat, changed-source rejection, a new snapshot ID, byte-for-byte restoration, corruption rejection with the destination preserved, and one limitation of checksum-based verification.

[Projects](../README.md) · [Testing](../../notes/testing.md) · [Vault](../../notes/vault.md)
