## Task 1: Environment Setup, Inventory Basics, and Verification

**Objectives:**
- Install and configure Ansible on a control node (locally via a Docker container or a local Linux environment).
- Understand Ansible’s inventory concept and verify connectivity to managed hosts.
- Use ad‑hoc Ansible commands to confirm installation and environment readiness.

**Lab Steps:**

1. **Dockerized Ansible Control Node (Optional):**  
   Create a Docker container with Ansible installed. For instance, use an official Python image and install Ansible:
   ```bash
   docker run -it --name ansible-control python:3.9 bash
   # Inside the container:
   pip install ansible
   ```
   Alternatively, install Ansible directly on your Linux box via package manager.

2. **Basic Inventory Setup:**  
   Create an `inventory.ini` file:
   ```ini
   [webservers]
   web1 ansible_host=192.168.56.101
   web2 ansible_host=192.168.56.102
   ```
   (Adjust IPs to match your environment.)

3. **Ping Your Hosts with Ad-hoc Commands:**  
   From the Ansible control node, run:
   ```bash
   ansible all -i inventory.ini -m ping
   ```
   This verifies that Ansible can communicate with listed hosts.

4. **Reflection/Documentation:**  
   In your lab notes, describe how Ansible’s control node interacts with managed hosts (SSH by default). Record any issues faced (e.g., missing SSH keys, user permissions) and how you resolved them.
