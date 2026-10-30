# Batches, delegation, and rollout boundaries

A configuration task describes a resource. Orchestration describes when work happens relative to other work and what conditions allow the workflow to continue.

## Different controls solve different problems

| Control | Controls | Example |
|---|---|---|
| `forks` | Maximum concurrent worker processes | Bound controller/target load |
| `serial` | Hosts admitted to a play batch | Roll out to one host at a time |
| `strategy: linear` | Task progression within a batch | Default task barrier across active hosts |
| `strategy: free` | Independent task progression per host | Suitable only without required inter-host barriers |
| `throttle` | Concurrency for selected work | Limit requests to a shared API |
| `delegate_to` | Where a task executes | Run an API request on the controller |
| `run_once` | A task once for the current batch | A batch-level coordination step |

Increasing forks does not make a dependency disappear. A play with `serial: 1` still admits one host at a time. The `free` strategy can violate assumptions that one host waits for another at each task.

## Serial and run_once

With `serial`, `run_once` runs once **per batch**. It is not automatically once for the entire play. If a workflow truly requires a global one-time step, consider a separate controller play or an explicit first-host condition and confirm it against limits, failures, and strategy.

A delegated task retains the original host's task context in important ways. `inventory_hostname` continues to identify the original host; connection-related variables may be evaluated for the delegated host. Inspect which host supplies each variable instead of assuming delegation changes the whole play target. The simulated inventory explicitly defines its delegated `localhost` under `controller`, so inventory-based connection paths remain available there.

## Shared resources are still shared

In the simulated inventory, `node_a` and `node_b` are aliases for one computer. Each writes into its own host-named directory. This avoids races over a shared file and lets you inspect per-host state. Delegation does not serialize concurrent writes to one controller-side file; use an explicit coordination pattern when sharing state.

## Define the rollout contract

Project 02 sets `serial: 1` and `any_errors_fatal: true`. Each host snapshots its current release, promotes the requested version, reads it back, and checks a simulated health condition. On failure it restores only that host and fails the run.

If node A succeeds and node B fails, node A remains on the new release while node B is restored. This is a partial rollout, not a global transaction. Recovery policy must decide whether to retry B, roll back A separately, or keep the mixed state temporarily.

`max_fail_percentage` is evaluated against a batch and triggers when the threshold is exceeded. Do not casually substitute it for an explicit stop-on-any-failure policy. A rescued failure also needs a final failure if it should activate rollout stopping.

## Move to real systems deliberately

Replace the simulated health condition with a bounded application probe, drain traffic before interruption, wait for readiness before admitting traffic, and identify the artifacts needed to reverse a deployment. Test the failure of recovery itself. Use disposable VMs before connecting the design to a real fleet.

<details><summary>Self-check: does serial: 1 roll back every earlier host when the current host fails?</summary>

No. It limits admission into batches. Rollback is application-specific work you must explicitly implement, including whether it affects one host or all previously deployed hosts.

</details>

Practice: [lab 11](../labs/lab11/README.md), [project 02](../projects/02-rolling-release/README.md). Reference: [Execution strategies](https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_strategies.html), [delegation](https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_delegation.html).
