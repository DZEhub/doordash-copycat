M04 MLOps : GitHub Actions - DoorDash MLOps Project

# **DoorDash Containerized Job 🍔 Complete CI/CD Pipeline**

![DOORDASH](./images/DoorDash-Logo.png)

## Introduction to DoorDash

**DoorDash** is a major on-demand delivery platform in the United States. Founded in 2013, DoorDash connects customers with restaurants, grocery stores, and convenience shops. Handling millions of orders daily, DoorDash relies heavily on automated, scalable, containerized services to guarantee reliable delivery operations.

To maintain fast development cycles, the DevOps team increasingly adopts CI/CD pipelines, especially for their microservices running in Docker. **GitHub Actions** has become the standard platform for automating builds, tests, and deployments.

## Your Task 🚀

You just joined the **DevOps team at DoorDash**. The company is migrating from traditional CI platforms to GitHub Actions, and your mission is to build their first **comprehensive GitHub Actions workflow** for one of their microservices.

Your goal is to create a **complete GitHub Actions CI/CD workflow** that automatically:

- **Clones the repository** from your fork
- **Builds the Docker image** for the delivery fee calculation service
- **Runs the Docker container** to verify that it starts correctly
- **Waits for the service to be ready** (critical for preventing connection errors)
- **Tests all API endpoints** using both curl-based smoke tests and pytest unit tests
- **Validates response structure and status codes** to ensure data integrity
- **Cleans up resources** (stops and removes containers)

This workflow will become the foundation of DoorDash's automated CI/CD strategy for its containerized microservices, ensuring that only working code is deployed to production.

## **Scenario 🧩**

DoorDash is introducing a new **Dynamic Delivery Fee Calculation** service. This service computes delivery fees based on distance and weight, and provides time estimates for deliveries.

- The service is written in **Python (FastAPI)** for high performance and automatic API documentation
- It is containerized using a **Dockerfile** included in the repo for consistent deployment across environments
- You must automate the build, container startup, and comprehensive endpoint testing using **GitHub Actions**
- The service exposes multiple endpoints that must be tested for correctness and performance

Every time a developer pushes new code or creates a pull request, the workflow should:

- Pull the latest changes
- Build the Docker image
- Run the container
- **Wait for the service to become ready** (with health check retries)
- Test each API endpoint with appropriate HTTP methods and payloads
- Validate response structure and business logic
- Clean up Docker resources

This ensures that the microservice is always functional, deployable, and meets production quality standards.

## **Project Structure 📂**

```text
doordash-copycat/
├── .github/
│   └── workflows/
│       └── ci.yml                    # Main CI/CD workflow (2 sequential jobs)
├── app/
│   ├── main.py                       # FastAPI application with all endpoints
│   └── __init__.py
├── tests/
│   ├── test_root.py                  # Tests for / and /status/ endpoints
│   ├── test_fee_calculation.py       # Tests for /calculate-fee/ endpoint
│   ├── test_health.py                # Tests for /status/ endpoint (health check)
│   └── conftest.py                   # Pytest configuration
├── Dockerfile                        # Docker image definition
├── requirements.txt                  # Python dependencies
└── README_description.md             # Project documentation
```

## **API Endpoints Reference**

The FastAPI service exposes the following endpoints:

| Endpoint                         | Method | Purpose                | Parameters                     | Response                                     |
| -------------------------------- | ------ | ---------------------- | ------------------------------ | -------------------------------------------- |
| `/`                            | GET    | Welcome message        | None                           | `{"message": "Welcome to..."}`             |
| `/status/`                     | GET    | Service health check   | None                           | `{"status": "Service is up and running"}`  |
| `/calculate-fee/`              | POST   | Calculate delivery fee | `distance_km`, `weight_kg` | `{"delivery_fee": float}`                  |
| `/estimate-time/{distance_km}` | GET    | Estimate delivery time | `distance_km` (URL param)    | `{"estimated_delivery_time_minutes": int}` |

**Base URL:** `http://localhost:8080/`

**Content-Type:** `application/json`

## **Part I: Smoke Tests (curl-based)**

### **Step 1: Fork and Clone the Repository**

- Fork this repository to your GitHub account: 👉 https://github.com/JedhaBootcamp/doordash-copycat
- Clone your fork locally to inspect the code and understand the structure

### **Step 2: Understanding the FastAPI Application**

The `app/main.py` file contains a FastAPI application with the following structure:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="🍔 DoorDash Delivery API",
    version="0.1",
)

class DeliveryFeeRequest(BaseModel):
    distance_km: float
    weight_kg: float

# Endpoints:
# GET /                               - Returns welcome message
# POST /calculate-fee/                - Calculates delivery fee based on distance and weight
# GET /estimate-time/{distance_km}   - Returns estimated delivery time in minutes
# GET /status/                        - Returns service status
```

**Fee Calculation Logic:**

- Base fee: $5.00
- Per km: $1.50
- Per kg: $0.50
- Formula: `delivery_fee = 5.00 + (1.50 * distance_km) + (0.50 * weight_kg)`

### **Step 3: Create the GitHub Actions Workflow**

Inside your repository, create:

```bash
.github/
└── workflows/
    └── ci.yml
```

### **Step 4: Workflow Configuration**

The `ci.yml` workflow is configured to:

**Trigger Events:**

- `push` to `main` or `develop` branches
- `pull_request` targeting the `main` branch

**Environment Variables:**

```yaml
env:
    IMAGE: ghcr.io/org/ml-app              # Docker image registry
    PYTHON_VERSION: "3.11"                 # Python version used in container
```

## **Part II: Unit Tests with Pytest**

In production environments, API tests are not written inside CI workflows. Instead, they are written as test files in the repository and the CI simply executes them. This approach:

- ✅ Keeps the workflow clean and maintainable
- ✅ Allows developers to run tests locally before pushing
- ✅ Enables version control and review of test changes
- ✅ Follows industry best practices and conventions

### **Test File Structure**

Tests are organized in the `tests/` directory with one test file per endpoint:

- __test_root.py__ - Tests for `/`, `/status/`, and `/estimate-time/{distance_km}` endpoints
- __test_fee_calculation.py__ - Tests for `/calculate-fee/` endpoint with payload validation
- __test_health.py__ - Tests for `/status/` endpoint (health check)

Each test file validates:

- ✅ Correct HTTP status codes (200, 400, 404, etc.)
- ✅ Correct JSON response structure
- ✅ Correct business logic behavior
- ✅ Edge cases and invalid inputs

## **Common Issues and Solutions**

### **Issue 1: Connection Reset Error (curl: (56) Recv failure: Connection reset by peer)**

**Problem:**

- Tests attempt to connect to the API immediately after starting the container
- The service has not finished initializing yet
- The port binding is not yet ready

**Root Cause:**

- Docker runs with `-d` flag (detached mode), so it returns immediately without waiting for the service to be ready
- FastAPI needs a few seconds to initialize, bind to the port, and start accepting connections

**Solution (Implemented):**

```yaml
- name: wait for service to be ready
  run: |
    echo "Waiting for service to be ready..."
    for i in {1..30}; do
      if curl -sSf http://localhost:8080/ 2>/dev/null; then
        echo "Service is ready!"
        exit 0
      fi
      echo "Attempt $i/30 - Service not ready yet, waiting..."
      sleep 2
    done
    echo "Service failed to start"
    docker logs fee-service
    exit 1
```

**How it works:**

- Polls the root endpoint (`/`) every 2 seconds
- Retries up to 30 times (60 seconds total wait time)
- Shows progress on each attempt
- If successful, continues with tests
- If failed, displays container logs for debugging

### **Issue 2: HTTP 307 Temporary Redirect on /calculate-fee**

**Problem:**

- Tests receive HTTP 307 status instead of 200
- Response indicates a temporary redirect

**Root Cause:**

- The endpoint URL was missing a trailing slash: `/calculate-fee` instead of `/calculate-fee/`
- FastAPI automatically redirects URLs without trailing slashes to URLs with trailing slashes
- HTTP 307 preserves the request method (POST in this case) during redirect

**Solution (Implemented):**

```yaml
# BEFORE (incorrect):
response = httpx.post("http://localhost:8080/calculate-fee", json=payload)

# AFTER (correct):
response = httpx.post("http://localhost:8080/calculate-fee/", json=payload)
```

**Best Practice:** Always include trailing slashes in FastAPI endpoint definitions and when calling them

### **Issue 3: HTTP 404 - Endpoint Not Found (/health)**

**Problem:**

- Tests expect a `/health` endpoint but it returns 404
- The endpoint does not exist in the application

**Root Cause:**

- The test file was written with an assumed endpoint that doesn't match the actual API
- The actual health check endpoint is `/status/` not `/health`
- API endpoints must match exactly what is defined in `app/main.py`

**Solution (Implemented):**

```python
# BEFORE (incorrect endpoint):
response = httpx.get("http://localhost:8080/health")

# AFTER (correct endpoint):
response = httpx.get("http://localhost:8080/status/")
```

**Why it matters:** Always inspect `app/main.py` to identify the exact endpoints before writing tests

### **Issue 4: Incorrect Response Key Names**

**Problem:**

- Tests fail with assertions about missing keys in JSON responses
- Example: `AssertionError: assert 'estimated_time' in {'estimated_delivery_time_minutes': 35.0}`

**Root Cause:**

- Test expects key `estimated_time` but API returns `estimated_delivery_time_minutes`
- Response keys must match the actual API implementation exactly
- Pydantic models define the exact keys returned by FastAPI endpoints

**Solution (Implemented):**

```python
# BEFORE (incorrect key name):
assert "estimated_time" in response.json()

# AFTER (correct key name):
assert "estimated_delivery_time_minutes" in response.json()

# BEFORE (incorrect payload keys):
payload = {"distance_km": 5, "time_minutes": 10}

# AFTER (correct payload keys):
payload = {"distance_km": 5, "weight_kg": 2}
```

__Reference Table:__

| Endpoint                         | Request Keys                   | Response Keys                       |
| -------------------------------- | ------------------------------ | ----------------------------------- |
| `/calculate-fee/`              | `distance_km`, `weight_kg` | `delivery_fee`                    |
| `/estimate-time/{distance_km}` | N/A (path param)               | `estimated_delivery_time_minutes` |
| `/status/`                     | N/A                            | `status`                          |
| `/`                            | N/A                            | `message`                         |

### **Issue 5: Workflow and Test File Linking**

**Problem:**

- Having separate `ci.yml` and `build_test.yml` files causes confusion and duplicate work
- Tests may run in parallel without proper sequencing
- Difficult to manage workflow dependencies

**Root Cause:**

- Separate workflow files run independently
- No dependency management between workflows
- Duplicate Docker build and container startup steps

**Solution (Implemented):**
Consolidate into a single workflow with two sequential jobs using the `needs` keyword:

```yaml
jobs:
  smoke-tests:    # Job 1: Curl-based endpoint tests
    runs-on: ubuntu-latest
    steps:
      # Build, run, and test with curl
      ...

  unit-tests:     # Job 2: Pytest tests
    needs: smoke-tests  # Wait for Job 1 to complete successfully
    runs-on: ubuntu-latest
    steps:
      # Build, run, and test with pytest
      ...
```

**Benefits:**

- ✅ Single workflow file to maintain
- ✅ Guaranteed sequential execution
- ✅ Job 2 only runs if Job 1 passes
- ✅ Clear dependencies and flow
- ✅ Better visibility in GitHub Actions UI

### **Issue 6: Indentation and Spacing in YAML**

**Problem:**

- Excessive spaces before comments
- Inconsistent indentation levels
- Incorrect nesting of job properties

**Root Cause:**

- YAML is whitespace-sensitive
- Manual editing can introduce formatting inconsistencies
- Tools may not properly validate indentation

**Solution (Implemented):**

- Standardized all indentation to proper YAML levels
- Reduced excessive spaces before comments
- Fixed nesting of `runs-on` and `steps` under job definitions

**YAML Best Practices:**

```yaml
jobs:
    job-name:                  # Job level: 4 spaces
        runs-on: ubuntu-latest # Job property: 8 spaces
        steps:                 # Steps level: 8 spaces
            - name: step name  # Step: 12 spaces
              run: command     # Step property: 14 spaces
```

## **Complete Workflow Structure**

The final consolidated workflow (`ci.yml`) implements a 2-job CI/CD pipeline:

**Job 1: smoke-tests**

- Triggered by: push to main/develop, pull requests to main
- Steps:
  1. Checkout code
  2. Build Docker image
  3. Run Docker container (detached mode, port 8080)
  4. Check container status and logs
  5. Wait for service to be ready (30 retries × 2 seconds)
  6. Test endpoint 1: GET /
  7. Test endpoint 2: POST /calculate-fee/ with JSON payload
  8. Stop container

**Job 2: unit-tests** (depends on smoke-tests success)

- Steps:
  1. Checkout code
  2. Build Docker image
  3. Run Docker container
  4. Wait for service to be ready
  5. Install test dependencies (pytest, httpx)
  6. Run pytest on all test files
  7. Stop and remove container
  8. Clean up Docker image

**Key Features:**

- ✅ Automatic waiting for service readiness
- ✅ Health checks with retry logic
- ✅ Comprehensive endpoint testing (smoke + unit tests)
- ✅ Resource cleanup (always runs even on failure)
- ✅ Clear logging for debugging
- ✅ Sequential job execution with dependency management

## **Testing Locally Before Pushing**

Before pushing to GitHub, test your code and workflow locally:

**1. Test the FastAPI application locally:**

```bash
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

**2. Test endpoints with curl:**

```bash
# Test root endpoint
curl http://localhost:8080/

# Test status endpoint
curl http://localhost:8080/status/

# Test calculate-fee endpoint
curl -X POST http://localhost:8080/calculate-fee/ \
  -H "Content-Type: application/json" \
  -d '{"distance_km": 5, "weight_kg": 2}'

# Test estimate-time endpoint
curl http://localhost:8080/estimate-time/10
```

**3. Test with Docker:**

```bash
# Build image
docker build -t doordash/delivery-fee-service .

# Run container
docker run -d --name fee-service -p 8080:8080 doordash/delivery-fee-service

# Check logs
docker logs fee-service

# Test endpoints (same curl commands as above)

# Stop and remove
docker stop fee-service
docker rm fee-service
```

**4. Run pytest locally:**

```bash
pip install pytest httpx

# Start the service first (as shown above)

# Then run tests
pytest -v tests/
```

## **Debugging Tips**

### **If workflow fails:**

1. **Check GitHub Actions logs:**

   - Go to repository → Actions tab
   - Click on the failed workflow run
   - Expand the step that failed
   - Read the full error message
2. **View Docker container logs:**

```bash
docker logs fee-service
docker logs fee-service --tail 50
docker logs fee-service -f  # Follow logs in real-time
```

3. **Verify endpoint URLs:**

   - Ensure trailing slashes match: `/endpoint/` not `/endpoint`
   - Check query parameters and request body keys
   - Validate content-type headers
4. **Check Python dependencies:**

```bash
pip install -r requirements.txt
python -c "import fastapi; print(fastapi.__version__)"
```

5. **Test endpoints manually:**

```bash
# Use curl with verbose output
curl -v http://localhost:8080/endpoint/

# Use httpx directly (same as tests)
python -c "import httpx; print(httpx.get('http://localhost:8080/').json())"
```

6. **Verify Docker port binding:**

```bash
docker ps  # Check if port 8080 is exposed
netstat -tlnp | grep 8080  # Check if port is listening
```

## **Key Learnings and Best Practices**

### **1. Service Readiness is Critical**

- Always wait for services to be ready before testing
- Use health check polling with retries
- Provide meaningful feedback on each attempt

### **2. Endpoint Consistency**

- API endpoint definitions must match exactly when calling them
- Trailing slashes matter in FastAPI
- Document all endpoints with their exact paths and methods

### **3. Response Validation**

- Test response structure, not just status codes
- Validate all response keys match expectations
- Test both happy paths and edge cases

### **4. Workflow Organization**

- Consolidate related jobs into single workflows
- Use `needs` keyword for dependency management
- Separate smoke tests from unit tests conceptually, but keep them in one file

### **5. YAML Formatting**

- Maintain consistent indentation (2 or 4 spaces, not mixed)
- Comments should be clear and concise
- Follow the platform's documentation for exact syntax

### **6. Resource Cleanup**

- Always clean up Docker resources (containers, images)
- Use `if: always()` to ensure cleanup runs even on failure
- Document what resources are created and how they're removed

### **7. Test Organization**

- One test file per endpoint or logical group
- Descriptive test function names
- Document the endpoint being tested in comments
- Use assertions that provide clear failure messages

## **Next Steps and Enhancements**

### **Future Improvements:**

1. **Add more test coverage:**

   - Test invalid inputs (negative distances, invalid JSON)
   - Test edge cases (zero values, very large numbers)
   - Test error responses (400, 404, 500)
2. **Performance testing:**

   - Measure API response times
   - Set performance thresholds (e.g., response < 100ms)
   - Monitor memory and CPU usage
3. **Integration with other tools:**

   - Push image to Docker registry (Docker Hub, GitHub Container Registry)
   - Deploy to Kubernetes or cloud platform
   - Generate coverage reports
   - Send notifications on failure
4. **Environment-specific testing:**

   - Test against staging and production environments
   - Use different test datasets for different environments
   - Validate against real data
5. **Security scanning:**

   - Scan Docker image for vulnerabilities
   - Check Python dependencies for known vulnerabilities
   - Validate API security headers
6. **Monitoring and alerting:**

   - Integrate with monitoring systems (DataDog, New Relic)
   - Set up alerts for workflow failures
   - Track historical test metrics

## **Summary**

This project demonstrates a complete, production-ready CI/CD pipeline for a containerized microservice using GitHub Actions. Through our work, we:

✅ **Solved Critical Issues:**

- Fixed connection reset errors by implementing proper service readiness checks
- Resolved HTTP 307 redirects by ensuring endpoint URLs match exactly
- Fixed 404 errors by validating endpoints exist in the API
- Corrected response validation by using exact key names

✅ **Implemented Best Practices:**

- Organized workflow into logical, sequential jobs
- Created comprehensive test coverage with both smoke and unit tests
- Implemented proper resource cleanup
- Added detailed logging and debugging information

✅ **Created Documentation:**

- Documented all API endpoints with request/response format
- Explained the root cause of each issue
- Provided solutions and best practices
- Included local testing and debugging procedures

**The workflow is now ready for production use and serves as a template for other microservices at DoorDash!**

# Other solutions (from jedha)

We've written the whole solution in this repo:

* [https://github.com/JedhaBootcamp/doordash-copycat-SOLUTIONS-GHA](https://github.com/JedhaBootcamp/doordash-copycat-SOLUTIONS-GHA)

You will see two workflows:

1. `ci-part-i.yaml`
2. `ci-part-ii.yaml` with the associated tests inside `/tests` folder

IMPORTANT: Notice that we specified:

```yaml
        env:
          PYTHONPATH: ${{ github.workspace }}
```

This is important to run and import specific modules inside the workspace.
