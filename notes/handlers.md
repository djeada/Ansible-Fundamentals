# Handlers and change notifications

A handler is a named task that runs after another task reports a change and notifies it. This is useful when a configuration file should trigger a reload but an unchanged file should leave the service alone.

Lab 07 simulates a reload with a receipt file. It does not restart any real service. Run it twice and observe that the receipt-writing handler runs only after the configuration changes.

```yaml
# Task fragment
- name: Update application configuration
  ansible.builtin.copy:
    content: "{{ course_message }}\n"
    dest: "{{ training_root }}/lab07/config.txt"
    mode: '0644'
  notify: Record simulated reload
```

## Notification is conditional on change

A successful task with `changed: false` does not notify its handler. If several tasks notify the same handler, Ansible normally runs that handler once at the next handler flush, per host. Handler definition order determines execution order, not the order of names in `notify`.

A loop is considered changed if any item changes. If a loop notifies multiple handlers, do not assume Ansible maps each changed item to only the corresponding handler.

## Timing matters

Ansible normally flushes handlers after the relevant task sections of a play. Use `ansible.builtin.meta: flush_handlers` when a subsequent task must observe the reloaded configuration. Lab 07 uses this explicitly before continuing.

A handler can run again after a later task changes something and sends a new notification. “Once” means once per pending notification flush, not an unconditional once for an entire playbook.

## Reload, restart, and service presence

For a real service, ensure `state: started` independently of the handler. A handler triggered only by file changes will not repair a stopped service if the file is already correct. Use a reload when the service supports it and the configuration change permits it; otherwise a restart may be necessary.

Likewise, lab 07's receipt is an event record. Deleting the receipt alone will not notify a handler because its triggering configuration did not change. If a file is required desired state, manage it with a normal task rather than relying only on an event.

## Failure and naming

A later failed task can prevent a notified handler from running for that host. `force_handlers` changes some failure behavior, but it cannot make an unreachable host available or turn a bad configuration into a valid one. Validate candidates before notification and plan the failure path deliberately.

Handlers share a play-level namespace, including those loaded from roles. Use descriptive unique names or a deliberate `listen` topic. A name collision can shadow a handler and make notifications difficult to diagnose.

<details><summary>Self-check: why is an unconditional service restart task a problem?</summary>

It restarts the service on every run, even when its configuration is unchanged. A normal task should maintain service presence; a handler should perform the change-triggered reload/restart when appropriate.

</details>

Practice: [lab 07](../labs/lab07/README.md). Reference: [Handlers](https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_handlers.html).
