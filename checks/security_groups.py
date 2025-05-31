import boto3

SENSITIVE_PORTS = [22, 3389]

def check_open_security_groups():
    ec2 = boto3.client('ec2')
    result = []

    response = ec2.describe_security_groups()
    for sg in response['SecurityGroups']:
        group_id = sg['GroupId']
        group_name = sg.get('GroupName', 'N/A')
        risky_rules = []

        for rule in sg.get('IpPermissions', []):
            from_port = rule.get('FromPort')
            to_port = rule.get('ToPort')
            ip_ranges = rule.get('IpRanges', [])

            if from_port in SENSITIVE_PORTS:
                for ip_range in ip_ranges:
                    if ip_range.get('CidrIp') == '0.0.0.0/0':
                        risky_rules.append({
                            'Port': from_port,
                            'CIDR': '0.0.0.0/0',
                            'Description': ip_range.get('Description', '')
                        })

        if risky_rules:
            result.append({
                'SecurityGroupId': group_id,
                'GroupName': group_name,
                'RiskyRules': risky_rules
            })

    return result
