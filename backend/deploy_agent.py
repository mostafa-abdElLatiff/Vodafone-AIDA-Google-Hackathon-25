#!/usr/bin/env python3
"""
Deployment script for Network Incident Resolution Agent
"""

import os
import sys
import argparse
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from deployment.deploy import main as deploy_main
from absl import app, flags

def deploy_network_incident_agent():
    """Deploy the Network Incident Resolution Agent"""
    
    print("🚀 Deploying Network Incident Resolution Agent...")
    print("=" * 60)
    
    # Set up command line arguments
    sys.argv = [
        'deploy_agent.py',
        '--create',
        '--project_id=vodaf-aida25lcpm-205',
        '--location=europe-west1',
        '--bucket=your-bucket-name'  # Replace with your actual bucket name
    ]
    
    try:
        # Run the deployment
        deploy_main(sys.argv)
        print("\n✅ Agent deployment completed successfully!")
        print("\nNext steps:")
        print("1. Note the agent endpoint URL from the deployment output")
        print("2. Update the frontend agent_client.py with the endpoint URL")
        print("3. Redeploy your frontend to Cloud Run")
        
    except Exception as e:
        print(f"\n❌ Deployment failed: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure you have the correct GCP permissions")
        print("2. Verify your project ID and location")
        print("3. Make sure the bucket exists and is accessible")
        print("4. Check that all dependencies are installed")

def list_deployed_agents():
    """List all deployed agents"""
    print("📋 Listing deployed agents...")
    print("=" * 40)
    
    sys.argv = [
        'deploy_agent.py',
        '--list',
        '--project_id=vodaf-aida25lcpm-205',
        '--location=europe-west1'
    ]
    
    try:
        deploy_main(sys.argv)
    except Exception as e:
        print(f"❌ Failed to list agents: {e}")

def delete_agent(resource_id: str):
    """Delete a deployed agent"""
    print(f"🗑️ Deleting agent: {resource_id}")
    print("=" * 40)
    
    sys.argv = [
        'deploy_agent.py',
        '--delete',
        '--project_id=vodaf-aida25lcpm-205',
        '--location=europe-west1',
        f'--resource_id={resource_id}'
    ]
    
    try:
        deploy_main(sys.argv)
        print("✅ Agent deleted successfully!")
    except Exception as e:
        print(f"❌ Failed to delete agent: {e}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Deploy Network Incident Resolution Agent')
    parser.add_argument('action', choices=['deploy', 'list', 'delete'], 
                       help='Action to perform')
    parser.add_argument('--resource-id', help='Resource ID for delete action')
    
    args = parser.parse_args()
    
    if args.action == 'deploy':
        deploy_network_incident_agent()
    elif args.action == 'list':
        list_deployed_agents()
    elif args.action == 'delete':
        if not args.resource_id:
            print("❌ Resource ID is required for delete action")
            return
        delete_agent(args.resource_id)

if __name__ == "__main__":
    main()
