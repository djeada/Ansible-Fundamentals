# Learning path and assessment

The outcome is the ability to explain, write, test, and debug a small Ansible automation workflow. Completing a command is evidence only when you can explain the resulting state.

## Prerequisites

You should be comfortable with shell paths, text files, basic Git, and the difference between a process and a service. YAML and Jinja are introduced here. No prior Ansible experience is required. Budget 20–40 minutes for an early lab, 40–60 minutes for a later lab, and 2–4 hours per project; these are planning estimates, not benchmarks.

## Three passes through each lab

1. **Predict:** identify the target hosts, input values, files that may change, and the expected second-run result.
2. **Observe:** run the reference, inspect the actual artifact, and compare it with your prediction.
3. **Transfer:** close the reference, make the requested extension, and explain how you would diagnose a failure.

Keep a short journal with the command, prediction, recap, observed state, and one correction to your understanding. Do not paste real credentials into a journal or issue.

## Sequence

| Stage | Read | Practice | Exit criterion |
|---|---|---|---|
| Model and setup | [Introduction](notes/intro.md), [inventory](notes/inventory.md), [ad hoc commands](notes/ad_hoc_commands.md) | Labs 01–02 | Trace controller → module → target and explain drift |
| Data and execution | [Playbooks](notes/playbooks.md), [variables](notes/variables_and_facts.md) | Labs 03–05 | Explain precedence, types, per-host conditions, and loop results |
| Configuration design | [Templates](notes/templates.md), [handlers](notes/handlers.md), [roles](notes/users_and_roles.md) | Labs 06–08, project 01 | Validate configuration and expose a small role interface |
| Secrets and recovery | [Vault](notes/vault.md), [errors](notes/error_handling.md) | Labs 09–10 | Explain encryption at rest, output protection, and recovery limits |
| Operations and evidence | [Orchestration](notes/orchestration.md), [testing](notes/testing.md) | Labs 11–12, projects 02–03 | Prove rollout stopping and restore integrity under failure |

## Compare with Bash

After an Ansible lab, run its Bash alternative using the commands in that lab's guide. Predict which responsibilities move into explicit shell code: input validation, data serialization, content/mode comparison, event handling, sequencing, and recovery. Use the [comparison guide](notes/bash_alternatives.md) to identify where a pure shell implementation has a narrower contract, such as private plaintext handling without Vault encryption.

Keep the same prediction/observation/transfer journal for both tracks. Compare artifacts by meaning; paths, default learning labels, and JSON formatting differ deliberately. Bash outputs are isolated under `.sandbox/bash/`, and the scripts need no Ansible installation.

## What changes when you move to SSH hosts?

The desired-state model is unchanged, but assumptions multiply. You need a real inventory, verified host keys, credentials, an appropriate target Python interpreter, and narrowly scoped privilege escalation. Package and service behavior depends on the operating system. Read [SSH and keys](notes/ssh_and_ansible_keys.md) before using an actual disposable VM.

Do not simply change the supplied local inventory to production hosts. The training guard intentionally rejects non-local connections; make a separate VM exercise and explicitly review every target and privileged task.

## Project assessment rubric

Use the same scale for each project. A reference implementation is a baseline; a good extension should add observable behavior and tests.

| Dimension | 0 · Missing | 1 · Developing | 2 · Complete |
|---|---|---|---|
| Correctness | Command fails or state is wrong | Happy path works | Output contract is independently verified |
| Repeatability | Re-running damages state | Mostly stable | Second run has zero unintended changes |
| Failure behavior | Errors are hidden | Error is visible | Failure leaves a documented state and is tested |
| Interface | Inputs are hidden | Inputs are documented | Inputs have defaults, types, and validation |
| Explanation | Copied code without reasoning | Describes tasks | Explains tradeoffs, limits, and recovery |

Aim for at least 8/10 with no zero in correctness or failure behavior. Attach a short evidence log to your project: initial run, second run, injected failure, recovery, and one limitation you would address before using real infrastructure.

## Suggested teaching format

For a workshop, pair learners and alternate driver and reviewer roles every lab. Ask the reviewer to predict `changed`, `skipped`, and `failed` before execution. Stop after lab 07 for a design review: which changes should notify a service reload, and which should not?

Use [debugging challenges](exercises/README.md) as short assessments. The [flashcards](flashcards/intro.md) are for retrieval practice after an experiment, not a substitute for running it.

## Extension ladder

1. Add a new validated input and a test that rejects an invalid value.
2. Add a verifier that reads state without repairing it.
3. Separate development and staging inventories without duplicating a role.
4. Replace a simulated health check with a bounded `ansible.builtin.uri` check on a disposable VM.
5. Add service configuration validation, SSH credentials, and privilege escalation only when the earlier contracts still pass.

For database extensions, specify consistency, retention, restore authorization, and test isolation before selecting a module. A file checksum demonstrates byte integrity; it does not demonstrate application-level recoverability.
