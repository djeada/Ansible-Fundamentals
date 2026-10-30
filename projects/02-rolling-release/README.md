# Project 02 · Rolling release with explicit rollback

Build a deployment workflow that can succeed, fail visibly, recover one host, and stop before admitting later batches. The local reference models a release as a file; no real processes or traffic are changed.

## Brief before the reference

Use two inventory hosts and separate state for each. Bootstrap a starting release without overwriting later deployments. For each host, snapshot the previous release, promote a requested version, read the resulting bytes, and evaluate health. If health fails, restore the snapshot and leave the overall deployment failed. Admit one host per batch and stop after a failed batch.

You must demonstrate both a failure on the first host and a failure after an earlier host has succeeded. State precisely which hosts are restored and which remain on the new version.

## Initialize and deploy

Always specify the simulated inventory:

```bash
ansible-playbook -i inventories/simulated/hosts.yml projects/02-rolling-release/bootstrap.yml
ansible-playbook -i inventories/simulated/hosts.yml projects/02-rolling-release/deploy.yml
ansible-playbook -i inventories/simulated/hosts.yml projects/02-rolling-release/deploy.yml
cat .sandbox/projects/rollout/node_a/release.txt
cat .sandbox/projects/rollout/node_b/release.txt
```

Both hosts should contain v2 after the normal deployment. The repeated deploy should report zero changes. Bootstrap seeds v1 only when state is absent; it is not a reset operation.

## Fail the first batch

The following command deliberately exits nonzero:

```bash
ansible-playbook -i inventories/simulated/hosts.yml projects/02-rolling-release/deploy.yml \
  -e '{"course_release": "v3", "course_failure_host": "node_a"}'
```

Read both release files. Node A should have been restored to v2; node B should remain v2 because the later batch was not admitted. The rescue path ends with an explicit failure after restoration, preserving the failed deployment outcome.

## Fail a later batch

```bash
ansible-playbook -i inventories/simulated/hosts.yml projects/02-rolling-release/deploy.yml \
  -e '{"course_release": "v3", "course_failure_host": "node_b"}'
```

This command also deliberately exits nonzero. Node A succeeds and remains on v3. Node B fails and is restored to v2. The reference performs **per-host rollback**; it does not roll back earlier successful batches.

Recover by deploying the same release without the failure injection:

```bash
ansible-playbook -i inventories/simulated/hosts.yml projects/02-rolling-release/deploy.yml \
  -e course_release=v3
```

Both hosts should now contain v3. Repeat that command to prove stable convergence.

## Explain the state machine

| Transition | State retained |
|---|---|
| Snapshot → successful promotion | Requested release on this host |
| Promotion → failed health check → successful restore | Previous release on this host; failed overall run |
| Earlier host succeeds, later host fails | Mixed versions until a deliberate follow-up action |
| Restore itself fails | Failed run with uncertain host state requiring investigation |

`serial: 1` limits admission. `any_errors_fatal: true` stops subsequent batches after the explicit failure. A successful rescue without that final failure would undermine the intended stop policy.

## What this simulation does and does not establish

Both aliases run on one machine. The health failure is a deterministic injected condition; the file read checks the deployed bytes. This proves ordering, state restoration, and exit behavior. It does not prove SSH resilience, load-balancer draining, process readiness, database compatibility, or availability during deployment.

Warm check mode predicts file changes on an initialized system and skips post-promotion health assertions. Bootstrap must run before deploy because deploy requires a real previous release to snapshot.

## Extensions

1. Add a read-only verifier for all host versions and a documented policy for partial rollouts.
2. Add a global rollback command that explicitly targets earlier successful hosts. Test that it does not erase unrelated state.
3. On disposable VMs, replace the simulated health condition with `ansible.builtin.uri` retries and add drain/rejoin operations. Define what happens if rollback or the health probe is unreachable.

Submit evidence for v1 → v2, an unchanged repeat, first-batch failure, later-batch failure, and recovery. Use [the rubric](../../CURRICULUM.md#project-assessment-rubric) and explain the mixed-version outcome.

[Projects](../README.md) · [Orchestration](../../notes/orchestration.md) · [Error handling](../../notes/error_handling.md)
