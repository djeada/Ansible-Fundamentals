# Contributing learning materials

Changes should help a learner explain and verify behavior. Keep the local track runnable with builtin modules, no sudo, and generated output under `.sandbox/`. Document optional external-system exercises separately with explicit prerequisites.

## A good lab contribution

A lab needs a concrete outcome, prerequisites, a prediction question, exact root-relative commands, observable artifacts, one failure/drift experiment, an explanation, and a transfer exercise. State expected nonzero exit statuses explicitly. Link the relevant notes and the previous/next exercise.

Use fully qualified module names, named plays/tasks, typed inputs, quoted permission modes, deterministic templates, and early input assertions. Prefer state-aware modules to shell commands. Avoid secrets, real personal data, public deployment, and unbounded external dependencies in examples.

A lab also needs one self-contained `alternative.sh` and a Bash comparison section. Keep all shell functions, data, and templates inside that lab file; do not source helpers or load other course files. Keep the shell runtime to Bash 3.2+ and the documented Unix utilities; explain narrower contracts rather than inventing JSON parsers or cryptography. Preserve `.sandbox/bash/` isolation, and add observable checks to `scripts/verify_bash.py` when behavior changes. ShellCheck is a developer check, separate from the runtime dependencies.

A role should document its public inputs, defaults, supported environment, outputs, and failure behavior. Add directories only when needed. Tags select work; dependency versions belong in requirements or Git references.

## Validate a change

With `.venv` active, run:

```bash
python scripts/check_content.py
yamllint -s .
python scripts/verify.py --syntax-only
python scripts/verify.py
python scripts/verify_bash.py
shellcheck labs/lab*/alternative.sh scripts/bash/cleanup.sh
```

The full suite creates a temporary copy and tests observable state and meaningful failure paths. It must not delete or rewrite a learner's original sandbox. If your environment blocks local sockets/processes, run the static checks and use CI for runtime validation; state that limitation accurately in the pull request.

When changing a behavior, add or update a corresponding assertion in `scripts/verify.py`. Do not assert only that the changed task appeared in the log. Read artifacts, test a repeat, and test recovery when relevant. Keep intentionally failing exercises out of the default happy path, and verify failures by both exit status and a specific expected error.

## Review checklist

- Do the commands work from the repository root with the documented dependency range?
- Are the target hosts and changed paths obvious?
- Does an identical repeat avoid unintended changes?
- Are cold-check limitations distinguished from warm-check behavior?
- Does a failed operation leave a documented state and honest exit status?
- Are local simulations clearly distinguished from VM/service/database guarantees?
- Do notes, lab instructions, references, and the learning path agree?

## Pull requests

Describe the learner-facing problem, the resulting behavior, and the evidence used to verify it. Include version and platform information for runtime checks. Keep screenshots and logs free of secrets. Cite official upstream documentation when semantics or compatibility change.
