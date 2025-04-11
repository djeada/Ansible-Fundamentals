## Task 7: Writing Custom Ansible Modules (in Python)

**Objectives:**
- Understand how to write a custom module in Python.
- Integrate the module into a playbook to perform a specialized operation.
- Learn module return structures and error handling.

**Lab Steps:**

1. **Create a Custom Module File:**  
   Inside a `library/` folder in your Ansible project, create `hello_module.py`:
   ```python
   #!/usr/bin/python

   from ansible.module_utils.basic import AnsibleModule

   def main():
       module = AnsibleModule(
           argument_spec=dict(
               name=dict(type='str', required=True)
           )
       )
       name = module.params['name']
       message = f"Hello, {name}!"
       module.exit_json(changed=False, msg=message)

   if __name__ == '__main__':
       main()
   ```

2. **Use the Custom Module in a Playbook:**
   ```yaml
   - name: Test Custom Hello Module
     hosts: localhost
     tasks:
       - name: Run Hello Module
         hello_module:
           name: "Ansible Learner"
         register: hello_out

       - debug:
           msg: "{{ hello_out.msg }}"
   ```

3. **Verification:**
   - Run the playbook and check if the custom message is printed.
   - Adjust your module logic to handle errors or additional parameters if you wish.

4. **Reflection:**  
   Summarize how custom modules can help in specialized tasks. Compare that to using built‑in modules or roles.
