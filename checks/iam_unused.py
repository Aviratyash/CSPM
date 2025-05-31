import boto3
from datetime import datetime, timedelta

def check_unused_iam_entities(days=90):
    iam = boto3.client('iam')
    threshold_date = datetime.utcnow() - timedelta(days=days)
    results = []

    # Users
    users = iam.list_users()['Users']
    for user in users:
        name = user['UserName']
        last_used = iam.get_user(UserName=name)['User'].get('PasswordLastUsed')
        if not last_used or last_used < threshold_date:
            results.append({
                'Entity': name,
                'Type': 'User',
                'LastUsed': str(last_used),
                'Severity': 'Medium',
                'RiskScore': 6,
                'Remediation': 'Review this IAM user and consider deactivating or deleting if no longer in use.'
            })

    # Roles
    roles = iam.list_roles()['Roles']
    for role in roles:
        role_name = role['RoleName']
        used = iam.get_role(RoleName=role_name)['Role'].get('RoleLastUsed', {}).get('LastUsedDate')
        if not used or used < threshold_date:
            results.append({
                'Entity': role_name,
                'Type': 'Role',
                'LastUsed': str(used),
                'Severity': 'Medium',
                'RiskScore': 6,
                'Remediation': 'Review this IAM role and remove or rotate it if unused.'
            })

    return results
