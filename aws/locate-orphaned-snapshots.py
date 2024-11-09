import boto3
import os

def get_snapshots_without_volumes():
    # Initialize EC2 client with credentials
    ec2 = boto3.client(
        'ec2',
        aws_access_key_id='?????',
        aws_secret_access_key='???',
        aws_session_token='???', # aws_session_token is optional
        region_name='eu-west-1'  # e.g., 'us-west-1'
    )

    # Get all snapshots owned by the user
    snapshots = ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']
    
    # Get all volumes to check if they exist
    volumes = ec2.describe_volumes()['Volumes']
    volume_ids = {vol['VolumeId'] for vol in volumes}

    # Find snapshots where the source volume no longer exists
    orphaned_snapshots = []
    for snapshot in snapshots:
        if snapshot['VolumeId'] not in volume_ids:
            orphaned_snapshots.append({
                'SnapshotId': snapshot['SnapshotId'],
                'VolumeId': snapshot['VolumeId'],
                'StartTime': snapshot['StartTime'].strftime("%Y-%m-%d %H:%M:%S")
            })

    return orphaned_snapshots


if __name__ == "__main__":
    snapshots = get_snapshots_without_volumes()
    output_file = os.path.join(os.getcwd(), 'orphaned_snapshots.txt')
    
    with open(output_file, 'w') as file:
        if snapshots:
            file.write("Snapshots with non-existing volumes:\n")
            for snap in snapshots:
                file.write(f"Snapshot ID: {snap['SnapshotId']}, Volume ID: {snap['VolumeId']}, Created on: {snap['StartTime']}\n")
            print(f"Results written to {output_file}")
        else:
            file.write("All snapshots are associated with existing volumes.\n")
            print("All snapshots are associated with existing volumes. Results written to file.")
