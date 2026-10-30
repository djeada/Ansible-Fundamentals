# Terminology with boundaries

| Term | Meaning | Common confusion |
|---|---|---|
| Control node | Machine running the Ansible CLI/engine | It need not be one of the SSH targets |
| Managed node | Target of a connection/module operation | It usually does not need Ansible installed |
| Inventory | Host membership, groups, and connection/input data | It is not the list of tasks |
| Inventory alias | Logical name of a host | It can differ from its connection address |
| Pattern | Expression selecting inventory hosts | A limit can narrow but not expand a play's selection |
| Playbook | YAML list of plays | It is not just any YAML document |
| Play | Target host selection plus execution context and work | A role is not a play |
| Task | One module/action invocation with directives | A task name is a label, not executable logic |
| Module | Code implementing an operation and returning structured results | Not every module is inherently idempotent |
| Action plugin | Controller-side task behavior coordinating module work | Some work happens before a module reaches the target |
| Connection plugin | Transport/execution mechanism such as SSH or local | Local aliases do not create isolated hosts |
| Collection | Namespaced package of Ansible content | Installing core does not install every external collection |
| FQCN | Fully qualified collection name, such as `ansible.builtin.copy` | It identifies content, not a version |
| Role | Reusable directory of tasks and related content | It is not an OS group or an access permission |
| Fact | Discovered host information, or fact-like stored data | Cached data can be stale |
| Registered result | Host-specific result of a task | A loop normally returns per-item results under `results` |
| Handler | Task run after a change notification | It does not automatically maintain service presence |
| Template | Controller-rendered text based on variables | A source path and destination path refer to different machines |
| Lookup | Controller-side data retrieval | It does not read a remote file by default |
| Filter | Transformation used in an expression | Escaping is format-specific |
| Idempotence | Repetition does not keep changing resulting state | A green recap alone does not prove correct state |
| Convergence | Movement from observed state toward declared state | It is not automatic rollback |
| Drift | State differs from the desired declaration | A verifier should detect it without necessarily repairing it |
| Check mode | Supported modules predict changes | It may skip work or lack prerequisites |
| Diff mode | Supported modules display before/after differences | It can reveal secrets |
| Become | Privilege escalation on the target | Choosing a become user alone does not enable it |
| Vault | Encryption of Ansible data at rest | It does not encrypt the runtime destination automatically |
| Serial | Admission of hosts into play batches | It is not a global deployment transaction |
| Delegation | Execution of a task on another host | It does not automatically serialize shared writes |
| Rescue | Recovery tasks after a block task fails | It is not triggered for every class of error |
| Rollback | Explicit restoration of a previous state | A successful rescue message is not itself a rollback |
| Tag | Label used to select tasks | It does not pin a role dependency version |

Use the [notes index](README.md) for full lessons and [flashcards](../flashcards/intro.md) for retrieval practice.
