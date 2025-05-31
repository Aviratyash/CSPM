import boto3

def check_iam_users_without_mfa():
    iam = boto3.client('iam')
    response = iam.list_users()
    results = []

    for user in response['Users']:
        username = user['UserName']
        mfa = iam.list_mfa_devices(UserName=username)
        if not mfa['MFADevices']:
            results.append({
                'User': username,
                'MFAEnabled': False,
                'Severity': 'High',  # 🔴 Used for Slack alerts
                'RiskScore': 9,      # Optional scoring
                'Remediation': 'Enable MFA for this IAM user in IAM → Users → [User] → Security Credentials.'
            })

    return results
