## Task 10: Docker Security Best Practices

**Objectives:**
- Implement Docker security features (user namespace, capabilities, seccomp profiles).
- Explore minimal base images and best practices for secure Dockerfiles.
- Discuss scanning images for vulnerabilities.

**Lab Steps:**

1. **Run Containers with Limited Capabilities:**
   ```bash
   docker run -d --cap-drop=ALL --cap-add=NET_BIND_SERVICE \
     -p 8080:80 --name secure_nginx nginx:latest
   ```
   - Check container capabilities with `docker inspect`.

2. **User Namespace and Non-Root Containers (Optional):**
   - In your Dockerfile, create and switch to a non-root user:
     ```dockerfile
     FROM alpine
     RUN addgroup -S mygroup && adduser -S myuser -G mygroup
     USER myuser
     ```
   - Build and run the container. Check that processes run as `myuser`.

3. **Scan for Vulnerabilities:**
   - Use a tool like `docker scan <image>` or third-party scanners (Trivy, Clair) to identify known CVEs.

4. **Reflection:**  
   Note how reducing container privileges and scanning images helps protect against attacks. Record any complexities in adopting these security measures.
