<#
Part I: Smoke Tests
1. Fork and Clone the Repository
    Fork this repository to your GitHub account: 👉 https://github.com/JedhaBootcamp/doordash-copycat
    Then clone your fork locally to inspect the code.

2. Create the GitHub Actions Workflow
    Inside your repository, create:
        .github/
        └── workflows/
            └── ci.yml
        Copy
    3. Write the CI Pipeline (ci.yml)
#>
# Inside your repository, create:
# .github/
# └── workflows/
#     └── ci.yml
mkdir -p .github/workflows
New-Item -Path ".github/workflows/ci.yml" -ItemType "File" -Force

# add, commit and push the new file to your repository
git status && git add . && git commit -m "update ci.yml for 5th commit" && git push

<#
Part II: Writing Real API Tests Using Pytest
Now that you have implemented basic smoke tests for your service, the next step is to make the pipeline more robust and closer to real-world MLOps practices.

In production teams, API tests are not written inside the CI workflow. They are written in pytest test files inside the repository, and the CI simply runs them.
#>
# Create tests/ Folder
# Inside your repository, create:
# tests/
#     test_health.py
#     test_fee_calculation.py
#     test_root.py
mkdir -p tests
New-Item -Path "tests/test_health.py" -ItemType "File" -Force
New-Item -Path "tests/test_fee_calculation.py" -ItemType "File" -Force
New-Item -Path "tests/test_root.py" -ItemType "File" -Force

# add, commit and push the new file to your repository
git status && git add . && git commit -m "update ci.yml adding part II for testing using pytest - 6th commit" && git push