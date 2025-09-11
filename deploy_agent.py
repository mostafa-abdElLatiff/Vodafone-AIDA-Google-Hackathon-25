import os
import sys
import argparse
from pathlib import Path

# Add the project's root directory to the Python path
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

# Import the main function from the deployment module
try:
    from deployment import deploy
except ImportError as e:
    print(f"❌ Error importing deployment script: {e}")
    sys.exit(1)

def run_deployment_action(action, resource_id=None):
    """A helper function to run the deploy.py script with the correct arguments."""
    
    # Construct the command-line arguments list
    argv = [
        'deploy.py',
        f'--project_id=vodaf-aida25lcpm-205',
        f'--location=europe-west1',
        f'--bucket=aida-hackathon-team-5',
    ]

    # Add the action and resource_id flags
    if action == 'deploy':
        argv.append('--create')
    elif action == 'list':
        argv.append('--list')
    elif action == 'delete':
        argv.append('--delete')
        if not resource_id:
            print("❌ Resource ID is required for delete action")
            return
        argv.append(f'--resource_id={resource_id}')
    else:
        print("Invalid action.")
        return

    # Call the main function from deploy.py directly with the constructed arguments.
    # The absl.app.run() function handles the flag parsing internally.
    try:
        deploy.app.run(main=deploy.main, argv=argv)
    except Exception as e:
        print(f"\n❌ Deployment failed: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure you have the correct GCP permissions.")
        print("2. Verify your project ID, location, and bucket name.")
        print("3. Check that the 'backend' and 'configs' directories exist and are accessible.")

def main():
    """Main function to parse arguments and run actions."""
    parser = argparse.ArgumentParser(description='Manage Network Incident Resolution Agent')
    parser.add_argument('action', choices=['deploy', 'list', 'delete'], 
                        help='Action to perform')
    parser.add_argument('--resource-id', help='Resource ID for delete action')
    
    args = parser.parse_args()
    
    run_deployment_action(args.action, args.resource_id)

if __name__ == "__main__":
    main()