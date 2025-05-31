import boto3

def list_s3_buckets():
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    buckets = []

    for bucket in response['Buckets']:
        buckets.append({
            'Name': bucket['Name'],
            'CreationDate': str(bucket['CreationDate'])
        })

    return buckets
