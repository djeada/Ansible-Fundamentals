## Task 11: Docker in CI/CD Pipelines

**Objectives:**
- Integrate Docker builds and tests within a CI/CD platform (Jenkins, GitLab CI, GitHub Actions).
- Automate test runs and image pushes to a registry on commit.
- Employ tagging strategies for different environments (dev, staging, production).

**Lab Steps:**

1. **Sample CI File (GitLab CI Example):**
   ```yaml
   stages:
     - build
     - test
     - deploy

   build_image:
     stage: build
     script:
       - docker build -t registry.example.com/myproject/myapp:$CI_COMMIT_SHA .
       - docker push registry.example.com/myproject/myapp:$CI_COMMIT_SHA

   test_image:
     stage: test
     script:
       - docker run --rm registry.example.com/myproject/myapp:$CI_COMMIT_SHA pytest tests/

   deploy_prod:
     stage: deploy
     script:
       - docker pull registry.example.com/myproject/myapp:$CI_COMMIT_SHA
       - docker tag registry.example.com/myproject/myapp:$CI_COMMIT_SHA registry.example.com/myproject/myapp:latest
       - docker push registry.example.com/myproject/myapp:latest
   ```

2. **Local Testing (Optional):**
   - Use the same Dockerfile locally:
     ```bash
     docker build -t myapp:test .
     docker run myapp:test pytest tests/
     ```

3. **Reflection:**  
   Summarize how integrating Docker with CI/CD ensures consistent environments from development to production. Note how the “build once, run anywhere” principle fosters reliability.
