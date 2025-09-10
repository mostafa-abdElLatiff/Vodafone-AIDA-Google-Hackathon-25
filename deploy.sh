#!/bin/bash

# Network Incident Resolution Agent - Quick Deploy Script
# This script deploys the agent and provides instructions for frontend connection

echo "🚀 Network Incident Resolution Agent - Quick Deploy"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "backend/deploy_agent.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Set environment variables
export GOOGLE_CLOUD_PROJECT="vodaf-aida25lcpm-205"
export GOOGLE_CLOUD_LOCATION="europe-west1"
export GOOGLE_CLOUD_STORAGE_BUCKET="your-bucket-name"  # Replace with your actual bucket

echo "📋 Configuration:"
echo "  Project ID: $GOOGLE_CLOUD_PROJECT"
echo "  Location: $GOOGLE_CLOUD_LOCATION"
echo "  Bucket: $GOOGLE_CLOUD_STORAGE_BUCKET"
echo ""

# Test the deployment first
echo "🧪 Running pre-deployment tests..."
cd backend
python test_deployment_connection.py

if [ $? -ne 0 ]; then
    echo "❌ Pre-deployment tests failed. Please fix issues before deploying."
    exit 1
fi

echo ""
echo "✅ Pre-deployment tests passed!"
echo ""

# Deploy the agent
echo "🚀 Deploying the agent..."
python deploy_agent.py deploy

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Agent deployed successfully!"
    echo ""
    echo "📋 Next steps:"
    echo "1. Note the agent endpoint URL from the output above"
    echo "2. Update frontend/agent_client.py with the endpoint URL"
    echo "3. Redeploy your frontend to Cloud Run:"
    echo "   gcloud run deploy network-incident-frontend --source frontend --platform managed --region europe-west1 --allow-unauthenticated"
    echo ""
    echo "🔗 Your agent is now ready to use!"
else
    echo "❌ Agent deployment failed. Please check the error messages above."
    exit 1
fi
