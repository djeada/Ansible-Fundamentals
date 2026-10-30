# Project 01 · Configuration-driven learning site

Build a small learning-journal page from environment data using one reusable role. The result is a real HTML artifact you can inspect and optionally serve locally. The Ansible automation should remain deterministic and should not need to know whether a web server will later publish the file.

## Brief before the reference

Create a role with a title, description, and destination as documented inputs. Render a page displaying those inputs, the selected environment, and the logical host name. Reject an unsupported environment or empty title before rendering. Escape text for HTML. Add independent assertions that read the rendered artifact and check its public contract.

The first run should create the page; an identical repeat should report zero changes. A manually damaged page should be repaired. The core project must run without sudo or an installed web server.

## Run the reference

From the repository root with `.venv` active:

```bash
ansible-playbook projects/01-learning-site/site.yml
ansible-playbook projects/01-learning-site/site.yml
ansible-playbook projects/01-learning-site/site.yml --check --diff
cat .sandbox/projects/site/index.html
ansible-playbook projects/01-learning-site/site.yml -e course_environment=staging
```

The [play](site.yml) reuses the same [role](../../roles/training_site/tasks/main.yml) as lab 08. Role defaults describe reusable inputs; the play supplies this project's title and destination. Environment membership is validated at the play boundary.

## Inspect it in a browser, optionally

```bash
python -m http.server 8080 --bind 127.0.0.1 --directory .sandbox/projects/site
```

Open `http://127.0.0.1:8080` and stop the server with Ctrl-C afterward. Choose another local port if 8080 is occupied. This is a manual preview server, not an Ansible-managed service or a deployment to a public host.

## Prove the contract

| Experiment | Expected result |
|---|---|
| Fresh real run | An HTML page with the configured title and environment |
| Identical repeat | `changed=0` |
| Warm `--check --diff` | No predicted changes |
| Edit the generated heading manually | Normal run repairs it |
| Pass `training_site_title` as an empty string | Input assertion fails |
| Pass a title containing `<script>` | Literal escaped text appears in the artifact |
| Pass `course_environment=production` | Environment assertion fails before rendering |

The automated verifier checks the artifact and escaping independently. An assertion inside a play is useful, but it can share the same incorrect assumption as the template, so inspect the actual output too.

## Design questions

- Which inputs belong to the role and which are environment policy in the play?
- Why should the role avoid embedding a current timestamp in every output?
- If you add a service, which changes require reload and which only change static content?
- How would you verify availability independently of file creation?

## Extensions

1. Add a list of learning resources and render stable ordering. Test a title containing quotes and angle brackets.
2. Add separate environment inventories while keeping one role. Avoid duplicating the HTML template.
3. On a disposable Linux VM, add package/service configuration, validate the server configuration before reload, and use a bounded HTTP probe. Preserve unprivileged rendering as a separate behavior.

For assessment, submit the play, role input documentation, initial/repeat/drift evidence, rejected-input evidence, and an explanation of why file correctness is different from service availability.

[Projects](../README.md) · [Templates](../../notes/templates.md) · [Roles](../../notes/users_and_roles.md)
