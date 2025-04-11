## Task 4: Variables, Facts, and Conditionals

**Objectives:**
- Use variables in Ansible playbooks to make them dynamic.
- Leverage Ansible facts (automatic host data) and conditionals for environment‑aware tasks.
- Demonstrate how to store variables in group/host vars files.

**Lab Steps:**

1. **Group Variables File:**  
   Create a file `group_vars/webservers.yml`:
   ```yaml
   server_port: 8080
   my_nginx_package: nginx
   ```
   Add a variable to specify a custom port or package name.

2. **Facts and Conditionals in a Playbook:**  
   Modify your existing `web.yml` to use a variable for the package name and to conditionally run tasks based on OS family:
   ```yaml
   - name: Deploy Web Server
     hosts: webservers
     become: true
     tasks:
       - name: Install Web Server
         package:
           name: "{{ my_nginx_package }}"
           state: present
         when: ansible_facts['os_family'] == "Debian"

       - name: Ensure correct port is in Nginx config
         lineinfile:
           path: /etc/nginx/sites-available/default
           regexp: 'listen\s+'
           line: "listen {{ server_port }};"
         notify: Restart Nginx
   ```
   (Use a `notify` to trigger a handler.)

3. **Handlers:**  
   At the end of your playbook:
   ```yaml
   handlers:
     - name: Restart Nginx
       service:
         name: nginx
         state: restarted
   ```

4. **Reflection:**
   Discuss how variables and conditionals increase reusability. Mention best practices for variables (e.g., storing secrets in Ansible Vault, which you’ll explore later).

