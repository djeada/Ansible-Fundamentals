# Evidence that automation works

A playbook that parses is not necessarily correct. A successful first run may still change on every repeat. A repeatable file can still contain the wrong configuration. Test these claims separately.

## Layers of evidence

| Check | Catches | Does not establish |
|---|---|---|
| Content/link checks | Missing files, broken local references, incomplete lab structure | Correct Ansible execution |
| YAML lint | Formatting errors and ambiguous YAML conventions | Correct modules or runtime behavior |
| `--syntax-check` | Playbook structure and many module/action resolution errors | Valid runtime variables or target prerequisites |
| `--list-hosts` | Unexpected host selection | Host reachability or desired state |
| First real run | Execution against an actual target state | Repeatability or application correctness |
| Second real run | Unintended repeated changes | Correct output if assertions are absent |
| Independent artifact assertions | Incorrect observable state | Every possible production failure |
| Failure injection | Defined recovery and stop behavior | Recovery from failures you did not test |

## Check mode has a dependency problem

On an empty sandbox, a directory-creation task predicts a change without creating the directory. A later template or copy can then lack a prerequisite. Registered values may be absent or represent predicted rather than real state. Some modules skip work entirely. A task can also explicitly set `check_mode: false` and run for real.

Therefore this course's automated suite performs a real converge and repeat first, then checks **warm check mode** on existing state. It does not claim every workflow supports a cold dry run. Verification that requires the newly written bytes is skipped during check mode and tested during real runs.

Diff mode is separate. It displays supported before/after content and can disclose secrets. Use `diff: false` for sensitive tasks.

## Run the repository checks

```bash
python scripts/check_content.py
yamllint -s .
python scripts/verify.py --syntax-only
python scripts/verify.py
```

The verifier makes a temporary copy without `.git`, `.venv`, or `.sandbox`. It runs commands with the current virtual environment's Ansible executables and the copied configuration. Learner-created artifacts in the original sandbox are preserved.

The full suite checks all twelve labs, site rendering and escaping, repeated convergence, warm check mode, deliberate drift, rejected typed input, handler notification, encrypted Vault input, successful rescue, staged rollouts, rollback after a failed health check, checksum integrity, and refused corrupted restores. CI runs it across the supported core versions.

## Verification without repair

Run lab 12 once, then edit its release manifest. `--tags verify` should fail because it reads state without rewriting it. A normal run repairs the file and then verifies it. These two modes answer different questions: “is it correct now?” and “can automation make it correct?”

## Bash alternative tests

`python3 scripts/verify_bash.py` is an independent standard-library test runner for the Bash track. The lab scripts themselves use Bash and standard Unix utilities. Tests copy only the twelve standalone scripts and cleanup into an empty course layout, reject shell imports, restrict their PATH to those utilities, check artifacts with a separate JSON parser, and ensure previews and verification-only runs do not repair or create state. CI runs the system Bash on both Linux and macOS; ShellCheck also checks the shell sources on Linux.

See the [Bash comparison guide](bash_alternatives.md) for the different validation and encryption boundaries. The self-contained Bash implementations are designed for local exercises, not a substitute for Ansible's complete module, inventory, and connection behavior.

## Next testing steps

When a role starts managing packages and services, test on the operating systems it claims to support. Containers can be useful for file/package work but may not represent an init system or kernel correctly. Use VMs for those contracts. Molecule is one possible role-testing framework; adopt it when its environment lifecycle helps, rather than adding it merely to wrap a file-only example.

For a real deployment, add application probes, timeout behavior, authorization failure, restore rehearsal, and recovery failure. Keep each check tied to a behavior that matters.

<details><summary>Self-check: is changed=0 enough to accept a deployment?</summary>

No. It only shows no reported mutation for the current inputs and target state. Independently read and validate the deployed artifact or application behavior, and ensure the intended hosts actually ran.

</details>

Practice: [lab 12](../labs/lab12/README.md). Reference: [Check and diff mode](https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_checkmode.html).
