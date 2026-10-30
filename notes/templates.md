# Templates are configuration interfaces

A template turns structured inputs into text on the controller and copies the rendered result to the managed host. Use `copy` for static bytes and `template` when content depends on variables. Source template paths are controller-side; the destination is on the selected target.

## Expressions, statements, and comments

| Jinja syntax | Purpose | Example |
|---|---|---|
| `{{ ... }}` | Emit a value | `{{ course_environment }}` |
| `{% ... %}` | Control rendering | `{% for service in services %}` |
| `{# ... #}` | Template-only comment | `{# Not present in output #}` |

A template does not execute once per inventory host on that host. Rendering happens on the controller with the host's variable context. A `lookup('file', ...)` therefore reads a controller file; use `slurp` to read target bytes.

## Serialize structured formats

Hand-built JSON can break when an input contains quotes, backslashes, or a newline. Lab 06 lets the serializer handle those details:

```jinja
{{ {'environment': course_environment, 'port': course_port, 'message': course_message} | to_nice_json }}
```

For an HTML page, use explicit `| e` escaping when placing input into text or attributes; the shared site role does this. Escaping for HTML, JSON, shell commands, and YAML solves different problems. A filter appropriate for one format is not a universal sanitizer.

## Validate before replacement

Lab 06 uses `template.validate` to run Python's JSON parser against a temporary candidate:

```yaml
# Task fragment
- name: Render validated JSON
  ansible.builtin.template:
    src: templates/app.json.j2
    dest: "{{ training_root }}/lab06/app.json"
    mode: '0644'
    validate: "{{ ansible_playbook_python }} -m json.tool %s"
```

`%s` is replaced by the temporary candidate path. The validator runs on the target, so its executable must exist there. This Python path is appropriate for the course's local connection; choose a target executable for a remote system. Shell features such as pipes are not available in `validate`.

Input assertions and output validation catch different defects. An integer port in range is an input contract. Valid JSON is a syntax contract. A successful HTTP request would be a runtime contract. None substitutes for the others.

## Keep rendering deterministic

Do not embed the current time into every render unless each run is intentionally a new release. Sort unordered inputs when order is irrelevant. Document how whitespace affects the target format. A file that changes on every run causes needless handlers and obscures real drift.

Defaults are for optional inputs. For mandatory credentials or identifiers, validate presence rather than quietly rendering an empty string.

<details><summary>Self-check: does valid JSON prove the application accepts the configuration?</summary>

No. The parser proves JSON syntax, not the application's schema or runtime semantics. Add schema checks or an application-specific validator, then a bounded health probe where appropriate.

</details>

Practice: [lab 06](../labs/lab06/README.md), [project 01](../projects/01-learning-site/README.md). Reference: [Template module](https://docs.ansible.com/projects/ansible/latest/collections/ansible/builtin/template_module.html).
