import boto3
import json

def check_lambda_roles_with_wildcards():
    lambda_client = boto3.client('lambda')
    iam = boto3.client('iam')

    functions = lambda_client.list_functions()['Functions']
    flagged = []

    for fn in functions:
        role_arn = fn['Role']
        role_name = role_arn.split('/')[-1]
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
                    flagged.append({
                        'FunctionName': fn['FunctionName'],
                        'RoleName': role_name,
                        'PolicyName': policy_name,
                        'WildcardActions': actions
                    })

    return flagged
