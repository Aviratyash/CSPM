import boto3
from botocore.exceptions import ClientError

def check_public_buckets():
    s3 = boto3.client('s3')
    try:
        buckets = s3.list_buckets()
    except ClientError as e:
        return {"error": str(e)}

    results = []
    for bucket in buckets['Buckets']:
        name = bucket['Name']
        public = False
        reasons = []

        # Check bucket ACL
        try:
            acl = s3.get_bucket_acl(Bucket=name)
            for grant in acl['Grants']:
                grantee = grant.get('Grantee', {})
                if grantee.get('URI') == 'http://acs.amazonaws.com/groups/global/AllUsers':
                    public = True
                    reasons.append('ACL grants public access')
        except ClientError as e:
            reasons.append(f"ACL error: {e.response['Error']['Message']}")

        # Check bucket policy
        try:
            policy = s3.get_bucket_policy(Bucket=name)
            public = True
            reasons.append('Bucket policy allows public access')
        except ClientError as e:
            if e.response['Error']['Code'] != 'NoSuchBucketPolicy':
                reasons.append(f"Policy error: {e.response['Error']['Message']}")

        results.append({
            'Bucket': name,
            'Public': public,
            'Reasons': reasons
        })

    return results
