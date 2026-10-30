# Ansible Fundamentals

Learn Ansible by predicting a change, applying it, inspecting the result, and recovering from a mistake. This repository is a practical course with explanatory notes, twelve runnable labs with Bash alternatives, and three projects with reference implementations.

The core track runs on your own machine. It uses `ansible.builtin` modules, a local connection, and generated files inside `.sandbox/`. You do not need Docker, a cloud account, SSH access, root privileges, or an external collection to complete it.

## Start in five minutes

Use Linux, macOS, or WSL with Python **3.12–3.14** and Git. Native Windows is not a supported control node for this course. Run every command below from the repository root; Ansible discovers `ansible.cfg` there.

```bash
git clone https://github.com/djeada/Ansible-Fundamentals.git
cd Ansible-Fundamentals
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
ansible --version
ansible-inventory --graph
ansible-playbook labs/lab01/playbook.yml
ansible-playbook labs/lab02/playbook.yml --diff
ansible-playbook labs/lab02/playbook.yml --diff
```

The second run of lab 02 should end with `changed=0`, `failed=0`, and `unreachable=0`. Inspect `.sandbox/lab02/managed.txt`, change it by hand, and run the playbook again. That repair is configuration convergence.

The dependency range supports **ansible-core 2.20 and 2.21**. It deliberately excludes the next minor release until validated. Check the [official Python support matrix](https://docs.ansible.com/projects/ansible/latest/reference_appendices/release_and_maintenance.html#ansible-core-support-matrix) when changing versions. `ansible-core` provides the engine and builtin plugins; the larger `ansible` package also bundles community collections.

## Run the Bash alternatives

Every lab also has an [independent Bash implementation](notes/bash_alternatives.md), using Bash 3.2+ and standard Unix utilities without Ansible, Python, or jq at runtime. Each lab guide includes commands and a comparison of the mechanisms.

```bash
bash labs/lab01/alternative.sh
bash labs/lab02/alternative.sh --check
bash labs/lab02/alternative.sh
```

Bash artifacts live separately under `.sandbox/bash/`. The alternatives explicitly implement change detection and recovery; the comparison notes identify boundaries such as Vault encryption and general JSON parsing. The developer test runner, `python3 scripts/verify_bash.py`, checks them independently on Linux and macOS in CI.

## Choose a route

| Your goal | Route | Evidence of progress |
|---|---|---|
| First contact | [Introduction](notes/intro.md), labs 01–03 | Explain a task result and override a variable |
| Write reliable automation | Labs 04–10, then project 01 | Validate inputs, use a role, avoid unnecessary reloads |
| Practice operations | Labs 11–12, projects 02–03 | Stop a failed rollout and reject a damaged backup |
| Review or teach | [Curriculum](CURRICULUM.md), [flashcards](flashcards/intro.md), [debugging challenges](exercises/README.md) | Predict behavior before running commands |
| Change this repository | [Contributor guide](CONTRIBUTING.md) | Run the same checks as CI |

## Labs

Each lab has prerequisites, a prediction prompt, exact commands, expected artifacts, a failure experiment, and an explanation of the result. Read its README before the playbook.

| Lab | Topic | Main skill |
|---|---|---|
| [01](labs/lab01/README.md) | Control node and inventory | Explain what `ping` actually proves |
| [02](labs/lab02/README.md) | Desired state and files | Measure idempotence and repair drift |
| [03](labs/lab03/README.md) | Variables and results | Override inputs and inspect `register` |
| [04](labs/lab04/README.md) | Facts and conditions | Select behavior using boolean expressions |
| [05](labs/lab05/README.md) | Lists, dictionaries, loops | Configure selected items without duplication |
| [06](labs/lab06/README.md) | Jinja and validation | Reject invalid inputs before replacing a file |
| [07](labs/lab07/README.md) | Handlers | Reload only after a relevant change |
| [08](labs/lab08/README.md) | Roles | Reuse an interface with documented defaults |
| [09](labs/lab09/README.md) | Vault and runtime secrets | Encrypt at rest and suppress sensitive output |
| [10](labs/lab10/README.md) | Blocks and recovery | Distinguish rescue from rollback |
| [11](labs/lab11/README.md) | Serial execution | Observe batches on two simulated hosts |
| [12](labs/lab12/README.md) | Verification and CI | Detect incorrect state independently of a write |

## Projects

| Project | What you build | What you must demonstrate |
|---|---|---|
| [01 · Learning site](projects/01-learning-site/README.md) | An environment-specific HTML artifact using a shared role | Correct output, escaped inputs, repeatability, drift repair |
| [02 · Rolling release](projects/02-rolling-release/README.md) | A two-host deployment simulator | Successful promotion, per-host rollback, later batches stopped |
| [03 · Backup and restore](projects/03-backup-restore/README.md) | Immutable JSON snapshots and checksum manifests | Byte-for-byte restoration and rejection of corrupted data |

Projects include a working reference and an open-ended brief. Attempt the brief before reading the implementation. Local aliases in project 02 share one computer: this teaches execution order and file state, not network isolation or real service availability. Project 03 uses fixture data; database consistency and PostgreSQL backup tooling are extension work.

## Notes and reference

Begin with the [notes index](notes/README.md). Keep the [command reference](notes/cheat_sheet.md) and [troubleshooting guide](notes/troubleshooting.md) nearby. The notes connect each concept to a runnable lab and a self-check question.

## Verify the course

```bash
python scripts/check_content.py
yamllint -s .
python scripts/verify.py --syntax-only
python scripts/verify.py
python scripts/verify_bash.py
```

The full verifier works in a temporary copy of the repository. It runs the labs and projects, repeats them to check idempotence, checks warm check mode, and tests drift repair, Vault decryption, rollback, and backup corruption. It leaves your working sandbox alone. Ansible needs a normal environment that permits child processes and local sockets; highly restricted execution sandboxes may support syntax checks only. CI runs the Ansible suite on Linux for both supported core versions and the Bash suite on Linux and macOS.

## Reset

Generated files live in `.sandbox/`, which Git ignores. The following command removes **all course output**, including your experiment files and local Vault exercises; copy anything you need first.

```bash
ansible-playbook playbooks/cleanup.yml
```

The course playbooks have no `become` tasks. Optional SSH and user-management examples in the notes explain how real managed systems differ and are not part of the local execution track.

## Contribute and reuse

Read [CONTRIBUTING.md](CONTRIBUTING.md) for the learning-material standard and checks. The original misspelled `notes/palybooks.md` URL remains as a pointer to its corrected replacement. The incomplete MySQL/container task has been retired; [its migration note](scripts/task_01/README.md) explains the replacement path.

Licensed under the [MIT License](LICENSE).
