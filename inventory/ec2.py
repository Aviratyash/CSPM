import boto3

def list_ec2_instances():
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances()
    instances = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_data = {
                'InstanceId': instance['InstanceId'],
                'InstanceType': instance['InstanceType'],
                'State': instance['State']['Name'],
                'AvailabilityZone': instance['Placement']['AvailabilityZone']
            }
            instances.append(instance_data)

    return instances
