# Templates Management

Ansible uses templates to dynamically generate files tailored to specific environments and servers. This feature leverages the powerful Jinja2 templating engine, enabling conditional logic, loops, variables, and more.

## Understanding Templates in Ansible

Templates allow the creation of dynamic files by injecting variables and logic directly into files that will be deployed to target hosts. Common uses include configuration files, system files, and scripts.

### Jinja2 Templating Basics

Ansible templates utilize Jinja2 syntax, which includes variables, conditionals, loops, and filters.

Example Jinja2 template (`config.j2`):

```jinja2
server_name = {{ server_name }}
port = {{ port }}
{% if enable_ssl %}
ssl_certificate = {{ ssl_cert_path }}
{% endif %}
```

Explanation:
- Variables (`server_name`, `port`) are replaced by their values at runtime.
- Conditional statements (`{% if %}`) include content based on variables.

### Rendering Templates with Ansible

Use the `template` module to render and deploy templates:

```yaml
- name: Deploy configuration from template
  template:
    src: config.j2
    dest: /etc/myapp/config.conf
```

Output example:
```
changed: [server1]
```
Interpretation:
- Indicates the template was rendered and deployed successfully.

## Variables in Templates

Variables are central to template functionality, making templates adaptable to various contexts.

### Defining Variables

Variables can be defined in multiple ways, including inventory, playbooks, roles (`defaults/main.yml`), or even gathered facts from target hosts.

Example in inventory file:

```
webserver ansible_host=192.168.1.10 server_name=example.com port=80 enable_ssl=true ssl_cert_path=/etc/ssl/cert.pem
```

### Accessing Variables

Variables defined are accessed within templates using double curly braces `{{ variable_name }}`.

Example:

```jinja2
User={{ username }}
UID={{ uid }}
```

## Conditionals and Logic

Conditional logic allows templates to adapt dynamically based on variable values.

Example conditional in Jinja2:

```jinja2
{% if user_is_admin %}
admin=true
{% else %}
admin=false
{% endif %}
```

This outputs `admin=true` if `user_is_admin` is true, otherwise it outputs `admin=false`.

### Loops in Templates

Loops are useful for generating repetitive sections:

```jinja2
{% for user in users %}
User={{ user.name }}
UID={{ user.uid }}

{% endfor %}
```

## Filters and Functions

Jinja2 offers built-in filters and functions for additional text processing capabilities.

Example filter usage (`default` filter):

```jinja2
port={{ custom_port | default(8080) }}
```

This sets the `port` to `8080` if `custom_port` is not defined.

### Mathematical Operations in Templates

Jinja2 supports mathematical operations directly within templates:

```jinja2
worker_processes={{ ansible_processor_vcpus * 2 }}
```

If `ansible_processor_vcpus` is 4, the rendered value would be 8.

## Advanced Template Usage

Templates can incorporate complex logic, such as dynamically generated configuration files based on environment conditions or hardware resources.

### Example of Advanced Template Logic

```jinja2
{% set total_memory_gb = (ansible_memtotal_mb / 1024) | round(0, 'floor') %}
memory_limit={{ total_memory_gb * 0.75 | round }}GB
```

Explanation:
- Calculates available memory from facts (`ansible_memtotal_mb`).
- Allocates 75% of memory to the application, rounded to the nearest GB.

## Diagram of Template Rendering Workflow

```
+--------------+
| Variables    |
+--------------+
      |
      v
+--------------+
| Template.j2  |
+--------------+
      |
      v
+--------------+
| Ansible      |
| template     |
| module       |
+--------------+
      |
      v
+--------------+
| Rendered File|
+--------------+
      |
      v
+--------------+
| Target Host  |
+--------------+
```

- Variables feed into the template.
- The Ansible template module renders this into a usable file.
- The rendered file is deployed to the target host.
