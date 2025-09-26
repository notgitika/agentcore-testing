#!/bin/bash

# Build and Push image to your existing ECR repository
set -e

REGION="us-east-1"
ACCOUNT_ID="998846730471" # this is gitikavj+agentcore@amazon.com; please replace with your own
REPO_NAME="agentcore-test"
IMAGE_TAG="latest"

echo "🚀 Building ARM64 image for Bedrock Agent Core..."
echo "📋 Account ID: $ACCOUNT_ID"
echo "📦 Repository: $REPO_NAME"
echo "🏗️ Architecture: ARM64 (required by Bedrock Agent Core)"

# Setup buildx for multi-architecture builds
echo "🔧 Setting up Docker buildx..."
docker buildx create --use --name multiarch-builder 2>/dev/null || docker buildx use multiarch-builder

# Authenticate Docker to ECR
echo "🔐 Authenticating to ECR..."
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com

# Build ARM64 image using buildx; this is required by agentcore runtime!
echo "🔨 Building ARM64 Docker image..."

ECR_URI="$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO_NAME:$IMAGE_TAG"

DOCKERFILE=${1:-runtime}

# Build and push directly
docker buildx build \
    --platform linux/arm64 \
    --tag $ECR_URI \
    --push \
    -f src/docker/Dockerfile.$DOCKERFILE \
    .

echo ""
echo "✅ Success! ARM64 Bedrock Agent Core image is ready:"
echo "📍 ECR URI: $ECR_URI"
echo "🏗️ Architecture: ARM64 ✓"
echo ""
echo "🖥️ Use this URI in Bedrock Agent Core console:"
echo "$ECR_URI"
echo ""
echo "🧪 Next steps:"
echo "1. Copy the ECR URI above"
echo "2. Go back to Bedrock Agent Core console"
echo "3. Update the 'Image URI' field with:"
echo "   $ECR_URI"
echo "4. Try creating the agent again"
echo ""