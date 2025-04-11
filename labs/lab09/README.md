## Task 9: Ansible Vault and Secrets Management

**Objectives:**
- Secure sensitive data (passwords, API keys) using Ansible Vault.
- Learn how to create, edit, and use vaulted files in playbooks.
- Explore best practices around storing and sharing vault passwords.

**Lab Steps:**

1. **Create a Vaulted File:**
   ```bash
   ansible-vault create secrets.yml
   ```
   Enter a vault password and in the file store something like:
   ```yaml
   db_password: "superSecureP@ss"
   ```

2. **Use the Vaulted Variable in a Playbook:**
   ```yaml
   - name: Vault Demo
     hosts: webservers
     vars_files:
       - secrets.yml
     tasks:
       - debug:
           msg: "The database password is {{ db_password }}"
     # Run with vault password:
     # ansible-playbook -i inventory.ini vault_test.yml --ask-vault-pass
   ```

3. **Editing and Encrypting/Decrypting:**
   - `ansible-vault edit secrets.yml`  
   - `ansible-vault encrypt secrets.yml` (if not already encrypted).

4. **Reflection:**  
   Document how Vault prevents sensitive data leaks. Explore potential CI/CD integration, passing vault passwords as environment variables, etc.
