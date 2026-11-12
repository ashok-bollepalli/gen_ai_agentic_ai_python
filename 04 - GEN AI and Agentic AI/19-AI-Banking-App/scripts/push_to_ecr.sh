#!/bin/bash
# Build the Docker image and push it to AWS ECR.
#
# Usage:   ./scripts/push_to_ecr.sh            (uses tag 1.0)
#          ./scripts/push_to_ecr.sh 1.1        (custom tag)
#
# Needs: AWS CLI (logged in with `aws configure`) and Docker running.

set -e   # stop on first error

REGION="ap-south-1"
REPO="bankbuddy"
TAG="${1:-1.0}"

# 1. Find your AWS account ID automatically
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGISTRY="$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com"
IMAGE="$REGISTRY/$REPO:$TAG"

echo "Image: $IMAGE"

# 2. Create the ECR repository (only first time; ignore error if it exists)
aws ecr create-repository --repository-name "$REPO" --region "$REGION" >/dev/null 2>&1 \
  && echo "Created ECR repo: $REPO" || echo "ECR repo already exists: $REPO"

# 3. Login Docker to ECR
aws ecr get-login-password --region "$REGION" \
  | docker login --username AWS --password-stdin "$REGISTRY"

# 4. Build (linux/amd64 because EKS nodes are x86, even if you use a Mac M1/M2)
docker build --platform linux/amd64 -t "$IMAGE" .

# 5. Push
docker push "$IMAGE"

echo ""
echo "Done! Use this in k8s/*.yaml:"
echo "  image: $IMAGE"
