## Task 2: Ad-hoc Commands, Modules, and Inventory Organization

**Objectives:**
- Explore commonly used Ansible modules (e.g., `ping`, `shell`, `package`, `service`).
- Use Ansible ad‑hoc commands to manage multiple hosts simultaneously.
- Organize inventory into groups and subgroups.

**Lab Steps:**

1. **Ad-Hoc Package Installation:**  
   Suppose you have a group of web servers that need `nginx`. Run:
   ```bash
   ansible webservers -i inventory.ini -m apt -a "name=nginx state=latest update_cache=true" --become
   ```
   (Use `yum` or `dnf` module if CentOS/RHEL.)

2. **Service Management:**  
   Start and enable the `nginx` service:
   ```bash
   ansible webservers -i inventory.ini -m service -a "name=nginx state=started enabled=yes" --become
   ```

3. **Inventory Group Hierarchy:**  
   Update your `inventory.ini` to have hierarchical groupings:
   ```ini
   [production:children]
   webservers

   [webservers]
   web1 ansible_host=192.168.56.101
   web2 ansible_host=192.168.56.102
   ```
   Now you can target `production` as a parent group.

4. **Reflection:**  
   Note how grouping helps scale environment management. Consider timesaving advantages of ad‑hoc commands for one‑off changes.
