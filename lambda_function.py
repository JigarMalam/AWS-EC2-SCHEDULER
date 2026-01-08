# ...existing code...
import boto3
import os

# Initialize the EC2 client (service first, region as kwarg)
region = os.environ.get('AWS_REGION', 'ap-south-1')
ec2 = boto3.client('ec2', region_name=region)

def lambda_handler(event, context):
    # This captures the action ('start' or 'stop') passed from EventBridge
    action = event.get('action')
    if action not in ('start', 'stop'):
        raise ValueError("event['action'] must be 'start' or 'stop'")

    # Filter for instances with Tag 'Env' = 'Dev'
    filters = [
        {
            'Name': 'tag:Env',
            'Values': ['Dev']
        }
    ]

    # Find the instances
    resp = ec2.describe_instances(Filters=filters)
    instances = [
        inst['InstanceId']
        for res in resp.get('Reservations', [])
        for inst in res.get('Instances', [])
    ]

    if not instances:
        return {'status': 'no-instances'}

    if action == 'start':
        ec2.start_instances(InstanceIds=instances)
    else:
        ec2.stop_instances(InstanceIds=instances)

    return {'status': action, 'affected': instances}
# ...existing code...