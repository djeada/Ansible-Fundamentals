# Retrieval practice

Answer aloud before opening each explanation. Then run the linked lab or change one input to test your answer. These cards focus on boundaries and failure modes rather than definitions alone.

## 01 · A ping succeeds. Is the web application healthy?

<details><summary>Check your answer</summary>

No. The builtin ping proves Python module execution through the configured connection. An HTTP/application probe tests a different contract.

[Revisit lab 01](../labs/lab01/README.md).

</details>

## 02 · node_a and node_b both use ansible_connection: local. How many isolated machines exist?

<details><summary>Check your answer</summary>

One shared computer, with two logical inventory aliases. Separate paths avoid file collisions; aliases do not isolate processes or networking.

[Revisit lab 11](../labs/lab11/README.md).

</details>

## 03 · The recap is green but says no hosts matched. Did configuration succeed?

<details><summary>Check your answer</summary>

No selected host ran the requested work. Inspect the active inventory, play pattern, and limit.

[Revisit lab 01](../labs/lab01/README.md).

</details>

## 04 · What should an unchanged second run tell you?

<details><summary>Check your answer</summary>

It should report zero unintended changes. Independently inspect correctness; zero changes alone can also mean nothing useful ran.

[Revisit lab 02](../labs/lab02/README.md).

</details>

## 05 · A file is manually edited. Is a changed result on the next run a failure of idempotence?

<details><summary>Check your answer</summary>

No. The starting state drifted. Repair is an expected change; a subsequent identical repeat should stabilize.

[Revisit lab 02](../labs/lab02/README.md).

</details>

## 06 · Why not use changed_when: false on every command?

<details><summary>Check your answer</summary>

It hides reported mutations and suppresses notifications. It does not remove side effects or make the operation state-aware.

[Revisit lab 02](../labs/lab02/README.md).

</details>

## 07 · Does -e course_port=9090 provide an integer?

<details><summary>Check your answer</summary>

No. key=value extra vars are strings. Pass typed JSON/YAML for the integer contract in lab 06.

[Revisit lab 06](../labs/lab06/README.md).

</details>

## 08 · Does ansible-inventory --host include every future play override?

<details><summary>Check your answer</summary>

No. It shows effective inventory data. Play/task/role parameters and extra vars in a later run can change effective values.

[Revisit lab 03](../labs/lab03/README.md).

</details>

## 09 · Why prefer ansible_facts["system"] over an injected top-level fact name?

<details><summary>Check your answer</summary>

It explicitly identifies the facts namespace and avoids depending on top-level fact injection behavior.

[Revisit lab 04](../labs/lab04/README.md).

</details>

## 10 · Can a skipped registered task lack stdout?

<details><summary>Check your answer</summary>

Yes. The result can contain skip metadata rather than fields from a completed command. Inspect structure before indexing.

[Revisit lab 03](../labs/lab03/README.md).

</details>

## 11 · Where does a loop put per-item results?

<details><summary>Check your answer</summary>

Usually under the registered result's results list. Each item carries its own result and loop data.

[Revisit lab 05](../labs/lab05/README.md).

</details>

## 12 · A service is disabled in input. Why does its old config remain?

<details><summary>Check your answer</summary>

A when condition can prevent a new write without declaring absence. Add explicit removal if disabled means the configuration must be absent.

[Revisit lab 05](../labs/lab05/README.md).

</details>

## 13 · Where is a Jinja template rendered?

<details><summary>Check your answer</summary>

On the controller, using the target host's variable context. The destination file is then managed on the selected target.

[Revisit lab 06](../labs/lab06/README.md).

</details>

## 14 · Does a file lookup read the remote host?

<details><summary>Check your answer</summary>

No. A file lookup reads on the controller. Use slurp or another target-side operation for remote bytes.

[Revisit lab 06](../labs/lab06/README.md).

</details>

## 15 · Why serialize JSON instead of concatenating it?

<details><summary>Check your answer</summary>

The serializer preserves types and escapes quotes, backslashes, and other string content correctly. Input and schema validation are still separate.

[Revisit lab 06](../labs/lab06/README.md).

</details>

## 16 · Does template.validate run through a shell?

<details><summary>Check your answer</summary>

No. The command receives the temporary file path through %s; shell features such as pipes are not interpreted.

[Revisit lab 06](../labs/lab06/README.md).

</details>

## 17 · Two changed tasks notify one handler before a flush. How often does it run?

<details><summary>Check your answer</summary>

Normally once for that host at the flush. A later change after the flush can notify it again.

[Revisit lab 07](../labs/lab07/README.md).

</details>

## 18 · Why does deleting only the reload receipt not rerun the handler?

<details><summary>Check your answer</summary>

The trigger configuration did not change. A handler responds to a notification; it does not independently maintain every artifact.

[Revisit lab 07](../labs/lab07/README.md).

</details>

## 19 · Does a role grant SSH or sudo permissions?

<details><summary>Check your answer</summary>

No. An Ansible role packages reusable content. Connection identity and privilege escalation are separate settings and policies.

[Revisit lab 08](../labs/lab08/README.md).

</details>

## 20 · Does become_user: root enable escalation?

<details><summary>Check your answer</summary>

No. become must be enabled, and the connection account must have an authorized escalation mechanism.

[Revisit lab 08](../labs/lab08/README.md).

</details>

## 21 · Do task tags pin a role version?

<details><summary>Check your answer</summary>

No. Tags select execution. Dependency requirements or Git references select versions.

[Revisit lab 08](../labs/lab08/README.md).

</details>

## 22 · Why keep ordinary public role inputs in defaults?

<details><summary>Check your answer</summary>

Role defaults are deliberately low precedence and easy for consumers to override. Internal high-precedence vars can make an interface unexpectedly rigid.

[Revisit lab 08](../labs/lab08/README.md).

</details>

## 23 · Does Vault automatically protect a rendered token file?

<details><summary>Check your answer</summary>

No. Vault protects encrypted stored input. Runtime plaintext needs suitable permissions, output suppression, and lifecycle controls.

[Revisit lab 09](../labs/lab09/README.md).

</details>

## 24 · Is Vault rekey the same as rotating the service token?

<details><summary>Check your answer</summary>

No. Rekey changes encryption credentials. Token rotation changes the credential used by the service.

[Revisit lab 09](../labs/lab09/README.md).

</details>

## 25 · Does rescue roll back earlier tasks?

<details><summary>Check your answer</summary>

No. Only explicit restoration tasks can reverse earlier changes. Lab 10 avoids promotion before validation; project 02 snapshots and restores.

[Revisit lab 10](../labs/lab10/README.md).

</details>

## 26 · Will unreachable hosts trigger ordinary block rescue?

<details><summary>Check your answer</summary>

No. Unreachable hosts and invalid task definitions are not ordinary failed-task recovery paths.

[Revisit lab 10](../labs/lab10/README.md).

</details>

## 27 · Why fail after a successful rollback?

<details><summary>Check your answer</summary>

To preserve that deployment failed and activate the intended stop policy, rather than treating recovery as deployment success.

[Revisit lab 10](../labs/lab10/README.md).

</details>

## 28 · With serial: 1, is run_once global?

<details><summary>Check your answer</summary>

No. It runs once per current batch. Design a separate global coordination step when that is the actual requirement.

[Revisit lab 11](../labs/lab11/README.md).

</details>

## 29 · Why might check mode fail on an empty sandbox?

<details><summary>Check your answer</summary>

Predicted prerequisites are not created, some modules skip work, and later reads can lack files or results. Warm check mode after convergence tests a narrower claim.

[Revisit lab 12](../labs/lab12/README.md).

</details>

## 30 · Why run verification separately from repair?

<details><summary>Check your answer</summary>

A repair can hide drift before inspection. Verify-only reads and assertions test whether the state is correct now without rewriting it first.

[Revisit lab 12](../labs/lab12/README.md).

</details>

For longer scenarios, use [the debugging challenges](../exercises/README.md) and [project rubric](../CURRICULUM.md#project-assessment-rubric).
