# Fork Improvements

This repository is a fork of the original **DocChat** project with additional improvements focused on containerization, automated code quality checks, and cloud deployment. 

## Added Features

### 🐳 Docker Support

Added Docker support to provide a consistent and reproducible environment for running the application.

### 🔍 Automated Code Quality Checks

Added **GitHub Actions** workflow for automated code quality validation using **Ruff**.

The workflow automatically:
- Runs Ruff code formatting
- Applies automatic linting fixes when possible
- Checks Python code quality on repository changes
- Commits formatting improvements to the branch

This helps maintain clean and consistent code throughout development.

### 🚀 Automated AWS Deployment

Implemented a CI/CD pipeline using **GitHub Actions** and AWS Elastic Container Registry with Elastic Container Service.

The deployment process includes:

1. Building a Docker image.
2. Pushing the image to **Amazon Elastic Container Registry (ECR)**.
3. Updating the **Amazon Elastic Container Service (ECS)** task definition with the new image version.
4. Deploying the updated container to **Amazon Elastic Container Service (ECS)**.
5. Waiting for ECS service stability after deployment.



