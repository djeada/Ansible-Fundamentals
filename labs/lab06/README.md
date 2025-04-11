## Task 6: Roles and Directory Structure

**Objectives:**
- Organize your playbooks into roles for better reuse and maintainability.
- Understand the **standard Ansible directory layout**.
- Convert an existing playbook into a role.

**Lab Steps:**

1. **Create a Role Skeleton:**  
   Use `ansible-galaxy init my_webserver_role`. This creates a structure:
   ```
   my_webserver_role/
   ├── tasks
   ├── handlers
   ├── templates
   ├── files
   ├── vars
   ├── defaults
   ├── meta
   ```

2. **Move Your Existing Logic:**  
   - Place your **installation tasks** into `my_webserver_role/tasks/main.yml`.  
   - Put your **templates** in `my_webserver_role/templates/`.  
   - Place your **restart handler** in `my_webserver_role/handlers/main.yml`.

3. **Role-based Playbook:**  
   Create `site.yml`:
   ```yaml
   - name: Webserver deployment
     hosts: webservers
     roles:
       - my_webserver_role
   ```
   Run:
   ```bash
   ansible-playbook -i inventory.ini site.yml
   ```

4. **Reflection:**  
   Explain why roles are critical for large projects. Document any changes needed to ensure your role works seamlessly (e.g., variable references).
