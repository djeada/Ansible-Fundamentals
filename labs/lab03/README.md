## Task 3: Writing Your First Playbook

**Objectives:**
- Understand Ansible playbooks, YAML structure, and tasks.
- Create a simple playbook to install and configure a web server.
- Execute the playbook and verify the results.

**Lab Steps:**

1. **Create a Simple Playbook (`web.yml`):**
   ```yaml
   ---
   - name: Deploy Nginx on webservers
     hosts: webservers
     become: true
     tasks:
       - name: Install Nginx
         apt:
           name: nginx
           state: latest
           update_cache: true

       - name: Start and enable Nginx
         service:
           name: nginx
           state: started
           enabled: true
   ```
   (Again, adapt to your OS package manager.)

2. **Run the Playbook:**
   ```bash
   ansible-playbook -i inventory.ini web.yml
   ```

3. **Verification:**
   - SSH into one of the webservers and check the status of Nginx.
   - Verify that your playbook’s tasks completed successfully in Ansible’s output.

4. **Reflection:**
   Write down the difference between **ad‑hoc** commands and **playbooks**. How do playbooks improve reproducibility and documentation?
