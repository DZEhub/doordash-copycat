GitHub Actions

# **DoorDash Containerized Job 🍔 30 min**

![DOORDASH](./images/DoorDash-Logo.png)

## Introduction to DoorDash

**DoorDash** is a major on-demand delivery platform in the United States. Founded in 2013, DoorDash connects customers with restaurants, grocery stores, and convenience shops. Handling millions of orders daily, DoorDash relies heavily on automated, scalable, containerized services to guarantee reliable delivery operations.

To maintain fast development cycles, the DevOps team increasingly adopts CI/CD pipelines, especially for their microservices running in Docker.

## Your Task 🚀

You just joined the **DevOps team at DoorDash**. The company is migrating from traditional CI platforms to GitHub Actions, and your mission is to build their first **GitHub Actions workflow** for one of their microservices.

Your goal is to create a **GitHub Actions workflow** that automatically:

- **Clones the repository**
- **Builds the Docker image** for the service
- **Runs the Docker container** to verify that it starts correctly
- **Tests all the API endpoints** directly from the workflow

This workflow will become the foundation of DoorDash’s automated CI/CD strategy for its containerized microservices.

## **Scenario 🧩**

DoorDash is introducing a new **Dynamic Delivery Fee Calculation** service. This service computes delivery fees based on distance, demand, weather, and real-time conditions.

- The service is written in **Python (FastAPI)**
- It is containerized using a **Dockerfile** included in the repo
- You must automate the build, container startup, and endpoint testing using **GitHub Actions**

Every time a developer pushes new code, the workflow should:

- Pull the latest changes
- Build the Docker image
- Run the container
- Ping each API endpoint while the container is running

This ensures that the microservice is always functional and deployable.

## **Your Tasks 📁**

You need to create a **GitHub Actions workflow** that:

- Checks out the repository (from your own fork)
- Builds the Docker image using the provided Dockerfile
- Runs the Docker container
- Tests all API endpoints using curl
  - Example: /, /health, /calculate-fee, etc.
  - (Refer to the code to identify the actual endpoints)

**IMPORTANT:**

- The app is an API running in a container — but you do not need to keep it alive. You only need to start the container, test its endpoints, and stop it. There is no deployment to production in this exercise.

# **Part I: Smoke Tests**

## **1. Fork and Clone the Repository**

- Fork this repository to your GitHub account:  👉 https://github.com/JedhaBootcamp/doordash-copycat
- Then clone your fork locally to inspect the code.

## **2. Create the GitHub Actions Workflow**

Inside your repository, create:

```
.github/
└── workflows/
    └── ci.yml
```

## **3. Write the CI Pipeline (ci.yml)**

Your workflow must:

- Trigger on push to main
- Build the Docker image
- Run the container
- Test all endpoints
- Stop and clean the container afterward

**HINT?**

- Regarding the container, try using the `-d` detached mode
- Also to test all endpoints, you can use `curl`

## **4. Validate the Workflow**

- Navigate to: **👉 GitHub Repository → Actions Tab**
- Verify that:
  - The workflow triggers correctly
  - The Docker image builds successfully
  - The container starts
  - Each tested endpoint returns a 200 OK (or expected status code)
  - All steps appear with a green ✅

If something goes wrong:

```Shell
docker logs fee-service
```

You can even add this as a step in your workflow for debugging.

## **Success Criteria ✅**

Your workflow is considered successful if:

- All GitHub Actions steps turn green
- The Docker image builds without error
- The container starts and stays healthy long enough for testing
- Every endpoint responds correctly using curl
- The workflow fails automatically if an endpoint is broken

# **Part II: Writing Real API Tests Using Pytest**

Now that you have implemented basic smoke tests for your service, the next step is to make the pipeline more robust and closer to real-world MLOps practices.

In production teams, API tests are not written inside the CI workflow. They are written in pytest test files inside the repository, and the CI simply runs them.

Your mission for this second part is to:

1. Create a tests/ Folder
   Inside your repository, create:

tests/
    test_health.py
    test_fee_calculation.py
    test_root.py
Copy
2. Write Pytest Tests for Each Endpoint
You will write Python tests that call the API running in Docker.

HINT
Your test suite should validate:

Correct status codes
Correct JSON structure
Correct behavior for valid inputs
Correct behavior for invalid inputs (e.g., 400 errors)
Write one test file per endpoint to match real industry conventions.

3. Update Your GitHub Actions Workflow
   Your workflow must now:

Build the Docker image
Run the API container
Wait for it to start (sleep 5)
Install test dependencies:
pip install pytest httpx
Copy
Run the tests:
pytest -v
Copy
This makes the pipeline fail automatically when a test fails — exactly how CI/CD operates in real MLOps systems.

Success Criteria for Part II 🎯
You have completed Part II when:

A tests/ folder exists
You wrote at least 3 test files
Each API endpoint is tested via pytest
GitHub Actions installs and runs pytest automatically
The pipeline fails when a test fails
All tests pass when the API behaves correctly
