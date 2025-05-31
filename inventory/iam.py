import boto3

def list_iam_users():
    iam = boto3.client('iam')
    response = iam.list_users()
    users = []

    for user in response['Users']:
        users.append({
            'UserName': user['UserName'],
            'UserId': user['UserId'],
            'CreateDate': str(user['CreateDate'])
        })

    return users
