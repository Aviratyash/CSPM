import boto3
import json

def check_iam_roles_with_wildcards():
    iam = boto3.client('iam')
    roles = iam.list_roles()
    flagged_roles = []

    for role in roles['Roles']:
        role_name = role['RoleName']
        policies = iam.list_attached_role_policies(RoleName=role_name)['AttachedPolicies']

        for policy in policies:
            policy_name = policy['PolicyName']
            version = iam.get_policy(PolicyArn=policy['PolicyArn'])['Policy']['DefaultVersionId']
            document = iam.get_policy_version(
                PolicyArn=policy['PolicyArn'],
                VersionId=version
            )['PolicyVersion']['Document']

            statements = document.get('Statement', [])
            if not isinstance(statements, list):
                statements = [statements]

            for stmt in statements:
                actions = stmt.get('Action', [])
                if isinstance(actions, str):
                    actions = [actions]
                if any(a == '*' or a.endswith(':*') for a in actions):
                    flagged_roles.append({
                        'RoleName': role_name,
                        'PolicyName': policy_name,
                        'WildcardActions': actions
                    })

    return flagged_roles
