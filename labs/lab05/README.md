## Task 5: Templates and Jinja2

**Objectives:**
- Use Jinja2 templates to manage configuration files dynamically.
- Render templates with Ansible variables and conditionals.
- Deploy templated files to managed hosts.

**Lab Steps:**

1. **Create a Jinja2 Template (`templates/index.html.j2`):**
   ```html
   <html>
   <head>
     <title>Welcome to {{ inventory_hostname }}</title>
   </head>
   <body>
     <h1>Hello from {{ ansible_facts['hostname'] }}!</h1>
     <p>Your server's OS is {{ ansible_facts['distribution'] }} {{ ansible_facts['distribution_version'] }}.</p>
   </body>
   </html>
   ```

2. **Playbook Task to Copy Template:**
   ```yaml
   - name: Copy custom index.html
     template:
       src: index.html.j2
       dest: /var/www/html/index.html
       owner: www-data
       group: www-data
       mode: '0644'
     notify: Restart Nginx
   ```

3. **Verify Templating:**  
   - Re-run your playbook and then browse to `http://<webserver_ip>:8080` (if you configured port 8080).  
   - You should see a dynamic page with the server’s hostname and OS details.

4. **Reflection:**  
   Note how Jinja2 helps create dynamic, environment‑specific configurations. Document potential use cases (e.g., large config files, credentials, etc.).

