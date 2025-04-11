# Ansible Fundamentals

Practice-based learning materials designed to help you gain hands-on experience with Ansible. This repository contains a comprehensive collection of notes, tutorials, and automation scripts—equipping beginners, system administrators, and DevOps professionals with the knowledge to automate IT tasks, manage configurations, and deploy applications efficiently.

## Features

- **Comprehensive Tutorials:**  
  Step-by-step guides covering Ansible’s core concepts—from simple configuration management to complex deployment workflows.

- **Real-World Use Cases:**  
  Learn how to apply Ansible in production-like environments, including tasks such as copying databases between environments using API-based utility containers for PostgreSQL backups and restores.

- **Interactive Labs & Examples:**  
  Hands-on labs provide practice with various Ansible modules, automation strategies, and integration techniques that complement your evolving IT infrastructure needs.

- **Extended Documentation:**  
  Detailed notes, accompanied by code samples and practical explanations, help bridge the gap between theory and real-world application.

## Typical Use Cases of Ansible

Ansible is a versatile automation platform that can be leveraged across many areas of IT operations. Below is a quick rundown of some common use cases and approaches:

- **Concept:**  
  Ansible is not only ideal for configuration management; it's also an effective tool for orchestrating complex operational tasks. Whether you’re managing deployments, handling backup and restore operations, or enforcing security policies, Ansible serves as the orchestrator for automating repetitive tasks.

- **Common Methods:**  
  Instead of relying on specialized modules for every specific task, you can often integrate conventional scripts and routines directly into your playbooks. This might include combining native command execution with API integrations to achieve desired outcomes.

- **Examples of Implementation:**

  - **Configuration Management:**  
    Use Ansible to ensure that systems are consistently configured, whether it’s managing users, installing software packages, or updating configuration files across environments.
  
  - **Application Deployment:**  
    Automate deployments by orchestrating steps such as code checkouts, service restarts, and load balancer configuration—all within a single playbook.
  
  - **Backup and Restore Operations:**  
    Trigger backup routines (e.g., via database dump utilities) and automate the restoration process by invoking API calls or running custom scripts as needed.
  
  - **Orchestration and Integration:**  
    Combine various tasks like running scripts on remote servers, executing API requests to external services, or coordinating updates across clusters to streamline multi-step processes.
  
Ansible acts as the central controller, coordinating these operations to replace manual, error-prone procedures with automated, repeatable, and scalable workflows.

## Labs

| #   | Title                                                                   | Link                                                                                                                                            |
|-----|-------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| 1   | Environment Setup, Docker Installation, and Verification                | [LAB](https://github.com/djeada/Ansible-Fundamentals/tree/main/labs/lab01)                                                                        |
| 2   | Basic Container Operations (Run, Stop, Remove, Inspect)                 | [LAB](https://github.com/djeada/Ansible-Fundamentals/tree/main/labs/lab02)                                                                        |
| 3   | Building Images with Dockerfiles                                        | [LAB](https://github.com/djeada/Ansible-Fundamentals/tree/main/labs/lab03)                                                                        |
| 4   | Docker Compose for Multi-Container Applications                         | [LAB](https://github.com/djeada/Ansible-Fundamentals/tree/main/labs/lab04)                                                                        |
| 5   | Networking in Docker (Bridged, Host, Overlay)                             | [LAB](https://github.com/djeada/Ansible-Fundamentals/tree/main/labs/lab05)                                                                        |
| 6   | Data Persistence with Volumes and Bind Mounts                           | [LAB](https://github.com/djeada/Ansible-Fundamentals/tree/main/labs/lab06)                                                                        |
| 7   | Docker Swarm for Container Orchestration                                | [LAB](https://github.com/djeada/Ansible-Fundamentals/tree/main/labs/lab07)                                                                        |
| 8   | Private Registry and Image Distribution                                 | [LAB](https://github.com/djeada/Ansible-Fundamentals/tree/main/labs/lab08)                                                                        |
| 9   | Monitoring and Logging in Docker                                        | [LAB](https://github.com/djeada/Ansible-Fundamentals/tree/main/labs/lab09)                                                                        |
| 10  | Docker Security Best Practices                                          | [LAB](https://github.com/djeada/Ansible-Fundamentals/tree/main/labs/lab10)                                                                        |
| 11  | Docker in CI/CD Pipelines                                               | [LAB](https://github.com/djeada/Ansible-Fundamentals/tree/main/labs/lab11)                                                                        |
| 12  | Advanced Docker Projects & Final Capstone                               | [LAB](https://github.com/djeada/Ansible-Fundamentals/tree/main/labs/lab12)                                                                        |

## Prerequisites

Before getting started, ensure you have the following installed and configured:

- **Ansible:**  
  A recent version of Ansible installed on your machine.
  
- **Utility Containers & APIs:**  
  Access to any required API services or containers (for example, a PostgreSQL container exposing backup/restore APIs).
  
- **Additional Tools:**  
  Git for version control, and any other dependencies needed for your custom modules or integrations.

## Installation

To set up your environment locally, follow these steps:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/ansible-fundamentals.git
   cd ansible-fundamentals
   ```

2. **Set Up Your Environment (Optional):**

   Create and activate a virtual environment if you plan to use local Python scripts alongside Ansible:
   
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**

   If there are any Python dependencies for your automation scripts, install them:
   
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Explore the repository as follows:

- **Read the Documentation:**  
  Navigate to the `docs` folder to review detailed notes and lab instructions.
  
- **Execute Playbooks:**  
  Run your Ansible playbooks from the command line to see live examples of configuration management and database operations.
  
- **Experiment & Innovate:**  
  Leverage the provided sample scripts and lab exercises to extend your automation capabilities.

## Repository Structure

Below is an overview of the repository’s structure:

```
ansible-fundamentals/
├── notes/                 # Detailed notes and tutorials
├── labs/                 # Practice labs and step-by-step guides
│   ├── lab1/             # Introduction to Ansible fundamentals
│   ├── lab2/             # Advanced automation tasks (e.g., database copying)
│   └── ...
├── playbooks/            # Ansible playbooks for various tasks
├── scripts/              # Supplementary scripts used for automation or API interactions
├── requirements.txt      # Python dependencies (if applicable)
├── README.md             # This file
└── LICENSE               # License information
```

## How to Contribute

Contributions are welcome! If you have ideas for new labs, improvements to existing tutorials, or additional automation scripts, please follow these steps:

1. Fork the repository.
2. Create your feature branch (e.g., `git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request describing your changes.

## License

This project is licensed under the [MIT License](LICENSE) – see the LICENSE file for details.
