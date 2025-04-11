## Task 8: Dynamic Inventories with Python

**Objectives:**
- Replace static inventory files with a Python script that dynamically generates hosts.
- Understand dynamic inventory use cases (cloud environments, Docker containers, etc.).
- Manage Docker containers or cloud VMs on-the-fly.

**Lab Steps:**

1. **Create a Python Dynamic Inventory Script (`docker_inventory.py`):**
   ```python
   #!/usr/bin/env python3
   import json
   import subprocess

   def main():
       # Example: list running Docker containers and treat each as a host
       # This is a simplified example; adapt to your environment
       result = subprocess.run(["docker", "ps", "--format", "{{.Names}}"], capture_output=True, text=True)
       container_names = result.stdout.strip().split("\n")

       inventory = {
           "docker_hosts": {
               "hosts": container_names,
               "vars": {"ansible_connection": "local"}
           }
       }
       print(json.dumps(inventory))

   if __name__ == "__main__":
       main()
   ```
   Make it executable: `chmod +x docker_inventory.py`.

2. **Configure `ansible.cfg` to Use the Script:**
   ```ini
   [defaults]
   inventory = ./docker_inventory.py
   ```
3. **Run Ad-Hoc Command Against the Dynamic Inventory:**
   ```bash
   ansible docker_hosts -m ping
   ```
   You should see a response for each running container.

4. **Reflection:**  
   Discuss the power of dynamic inventory for ephemeral or cloud-based infrastructure. Note how Python knowledge helps build flexible integrations.

