import boto3

def check_s3_encryption_disabled():
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    findings = []

    for bucket in response['Buckets']:
        bucket_name = bucket['Name']
        try:
            s3.get_bucket_encryption(Bucket=bucket_name)
        except s3.exceptions.ClientError as e:
            error_code = e.response['Error'].get('Code')
            if error_code == 'ServerSideEncryptionConfigurationNotFoundError':
                findings.append({
                    'Bucket': bucket_name,
                    'Encryption': 'Disabled',
                    'Severity': 'High',
                    'RiskScore': 8,
                    'Remediation': 'Enable default encryption for this bucket in the S3 console under Properties > Default encryption.'
                })
    return findings
