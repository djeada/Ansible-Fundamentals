# Debugging challenges

Try these after the associated labs. Work in a copy or record your edits so you can restore the reference. For each challenge, submit the smallest correction, a prediction, actual artifact evidence, and a short explanation. Do not solve a failure by hiding it.

## 1 · The perpetually changing configuration

A teammate adds a current timestamp to a managed configuration template. Every run changes the file and notifies a service reload.

Your task: decide whether time belongs in the runtime configuration. Preserve a meaningful release identifier that changes only when a release is intentionally selected. Prove an identical second run is stable and a new release still changes it.

<details><summary>Hint and reference</summary>

Deterministic output is part of the configuration contract. Removing change reporting would hide the defect rather than fix it. See [templates](../notes/templates.md) and [handlers](../notes/handlers.md).

</details>

## 2 · A disabled service that keeps its old config

Enable the worker in lab 05, run it, then disable it and run again. The worker configuration remains.

Your task: implement the intended “disabled means absent” policy using a state-aware module. Prove both directions of the transition and preserve the enabled web configuration.

<details><summary>Hint and reference</summary>

The existing conditional only skips copy. Add an explicit absence declaration for disabled items. See [lab 05](../labs/lab05/README.md).

</details>

## 3 · A string pretending to be a boolean

A caller supplies `-e course_candidate_valid=false`. An author writes `when: course_candidate_valid` and assumes this is the boolean false.

Your task: define a strict typed-input contract or a deliberate string-to-boolean conversion policy. Test true, false, missing, and an unsupported value. Explain why native JSON extra vars are useful.

<details><summary>Hint and reference</summary>

key=value extra vars are strings. Modern core versions require a boolean condition. Do not rely on a nonempty string's truthiness. See [variables](../notes/variables_and_facts.md) and [lab 10](../labs/lab10/README.md).

</details>

## 4 · Recovery turns a failed deployment green

Remove the final failure task from project 02's rescue block in a disposable copy. Inject a health failure on node A.

Your task: observe the exit status and whether the next batch is admitted. Restore honest deployment failure while retaining successful per-host restoration. Independently read both release files.

<details><summary>Hint and reference</summary>

A successful rescue changes failure handling. Recovery and successful deployment are different outcomes. See [error handling](../notes/error_handling.md) and [project 02](../projects/02-rolling-release/README.md).

</details>

## 5 · A checksum that only agrees with itself

An author “verifies” a backup by computing its checksum twice immediately before restore and comparing the two values.

Your task: explain why this cannot detect corruption since backup creation. Keep a stored creation-time manifest, reject altered snapshot bytes before writing the destination, and prove a failed restore preserves an existing destination.

<details><summary>Hint and reference</summary>

A checksum needs an independent reference. It still does not prove authenticity when both data and manifest can be replaced. See [project 03](../projects/03-backup-restore/README.md).

</details>

## 6 · A verifier that repairs its evidence

A pipeline runs the full lab 12 playbook, then asserts the release file is correct. The team claims this detects pre-existing drift.

Your task: show how the configuration step masks drift, then add a verify-only run before repair. Keep failure visible, and document when repair should be a separate approved workflow in a real environment.

<details><summary>Hint and reference</summary>

Use `--tags verify` on an existing artifact and inspect the return code. See [lab 12](../labs/lab12/README.md) and [testing](../notes/testing.md).

</details>

[Learning path](../CURRICULUM.md) · [Troubleshooting](../notes/troubleshooting.md)
