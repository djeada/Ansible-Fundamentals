# Bash alternatives: the same lessons with explicit shell logic

Every lab has a runnable `alternative.sh` alongside its Ansible playbook. Use the pair to distinguish the automation concept from the framework feature that implements it. Bash scripts use Bash 3.2+ and ordinary Unix utilities: `dirname`, `stat`, `mkdir`, `chmod`, `cmp`, `mktemp`, `mv`, `rm`, and `uname`. They do not invoke Ansible, Python, jq, or an external collection. No sudo is used.

The **test runner** uses Python's standard library to inspect results independently. Python is a development/testing dependency, not a dependency of the Bash lab scripts. CI runs the alternatives on Linux and macOS, including the system Bash on each runner, and uses a restricted PATH containing only the listed Unix utilities during behavioral tests.

## Start without installing Ansible

From a clone of this repository:

```bash
bash labs/lab01/alternative.sh
bash labs/lab02/alternative.sh --check
bash labs/lab02/alternative.sh
bash labs/lab02/alternative.sh
```

Read each lab's Bash section before experimenting. Commands are shown relative to the repository root, but each script derives its workspace from its own location, so calling it by absolute path from another directory also works. Invoke scripts with `bash`; do not source the entry points into your interactive shell.

All Bash outputs live in `.sandbox/bash/labNN/`. Ansible outputs keep their existing locations. You can run the two implementations side by side without overwriting each other's artifacts.

## Compare the mechanisms

| Lab | Ansible mechanism | Bash implementation and boundary |
|---|---|---|
| [01](../labs/lab01/README.md#bash-alternative) | Inventory, local connection, Python ping module | One declared logical host and a running local shell; no inventory parser or remote probe |
| [02](../labs/lab02/README.md#bash-alternative) | `file` and `copy` modules | Explicit content/mode comparisons and same-directory candidate promotion |
| [03](../labs/lab03/README.md#bash-alternative) | Variable sources and `register` | Environment defaults and an explicit last-change result |
| [04](../labs/lab04/README.md#bash-alternative) | Gathered facts and `when` | Selected `uname` probes and an `if` condition |
| [05](../labs/lab05/README.md#bash-alternative) | Structured loops and conditions | Indexed arrays, an ordered loop, exact boolean-text validation |
| [06](../labs/lab06/README.md#bash-alternative) | Jinja serialization and output validation | Validated decimal input and a string serializer for a known JSON shape; no general parser |
| [07](../labs/lab07/README.md#bash-alternative) | Notifications and handler flush | An explicit branch after the configuration changes; no queue or deduplication |
| [08](../labs/lab08/README.md#bash-alternative) | Role defaults, tasks, and templates | A sourced rendering function with explicit arguments and HTML escaping |
| [09](../labs/lab09/README.md#bash-alternative) | Vault plus private runtime output | Private plaintext handling and hidden input; encrypted storage requires another tool |
| [10](../labs/lab10/README.md#bash-alternative) | Block, rescue, and always | Deliberate conditional recovery; no automatic rollback |
| [11](../labs/lab11/README.md#bash-alternative) | Inventory limits, serial batches, delegation | Known local aliases in an ordered loop with a stop-on-failure path |
| [12](../labs/lab12/README.md#bash-alternative) | Configure/verify tags and parsed JSON assertions | Separate verification mode with an exact canonical-file contract |

## Inputs

Environment variables are always text. Each script validates the values it consumes. These are explicit shell defaults and interfaces, not a recreation of Ansible's variable precedence rules.

| Input | Default / accepted values | Labs |
|---|---|---|
| `COURSE_ENVIRONMENT` | `development`; also accepts `staging` | 03, 06, 08 |
| `COURSE_MESSAGE` | `Hello from Bash`; any Bash string, including empty | 03, 06, 07 |
| `COURSE_WORKER_ENABLED` | `false`; exact `true` or `false` | 05 |
| `COURSE_PORT` | `8080`; canonical decimal text, 1025–65535 | 06 |
| `COURSE_SITE_TITLE` | `My first reusable Bash function`; nonempty | 08 |
| `COURSE_SITE_DESCRIPTION` | A default learning description | 08 |
| `COURSE_CANDIDATE_VALID` | `false`; exact `true` or `false` | 10 |
| `COURSE_RELEASE` | `v1`; `v` followed by digits | 11 |
| `COURSE_LIMIT` | Empty for both hosts; `node_a` or `node_b` | 11 |
| `COURSE_FAILURE_HOST` | Empty, `node_a`, or `node_b` | 11 |
| `COURSE_EXPECTED_VERSION` | `v1`; `v` followed by digits | 12 |

Lab 09 accepts `--prompt` or `--token-stdin` for a nonempty single-line dummy token. It does not use an environment variable for private input. Bash strings cannot contain NUL bytes. The JSON string serializer preserves UTF-8 and escapes other ASCII control bytes; its output is checked by an independent parser in the tests.

## Change reporting and preview

The [shared helpers](../scripts/bash/lib.sh) compare bytes with `cmp` and modes with the appropriate GNU or BSD `stat` interface. They create a private temporary candidate in the destination directory, set its mode, and promote it only after the write succeeds. Permission-only drift is also repaired. Repeated, unchanged state produces `SUMMARY changed=0 check=false`.

Every lab accepts `--check`. The script reports `WOULD_CHANGE` for supported mutations and creates no directories or files in that mode. This behavior is explicitly implemented for these small local operations; it is not a generic shell dry-run capability. Validation still runs, and reading a private input may still be necessary to compare it. Normal verification after a predicted write is skipped because the predicted bytes do not exist yet.

The helpers reject symlink destinations and linked sandbox ancestors, and keep paths beneath the fixed Bash sandbox. They are teaching primitives for a private local checkout, not a concurrent resource manager. Two simultaneous writers can race; no distributed locks, multi-host transactions, owner/group management, service management, or arbitrary JSON parsing is supplied.

`set -euo pipefail` catches some mistakes but does not provide Ansible's task result model or a universal exception mechanism. Use explicit success/failure branches around operations whose recovery is part of the design. The examples never use `eval` to parse input.

## Verify independently

With any suitable Python 3 environment for development checks:

```bash
python3 scripts/verify_bash.py
# Optional shell lint, when ShellCheck is installed:
shellcheck -x labs/lab*/alternative.sh scripts/bash/*.sh
```

The verifier copies the repository into a temporary path containing spaces. It checks syntax, first runs, stable repeats, cold and warm previews, content/mode drift, invalid input, JSON and HTML escaping, conditional handler behavior, private-file output suppression, serial stopping, verification without repair, rejected symlinks, and cleanup isolation. Your original sandbox is preserved.

## Reset only the Bash track

This removes all generated Bash output, including any practice token. It preserves Ansible artifacts and other files directly under `.sandbox/`.

```bash
bash scripts/bash/cleanup.sh --check
bash scripts/bash/cleanup.sh
```

The original `ansible-playbook playbooks/cleanup.yml` command still removes **all** course output, including the Bash track. Preserve experiment files before either cleanup.

[Notes index](README.md) · [Learning path](../CURRICULUM.md) · [Testing](testing.md)
