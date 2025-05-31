import boto3

def check_public_rds_instances():
    rds = boto3.client('rds')
    results = []

    dbs = rds.describe_db_instances()
    for db in dbs['DBInstances']:
        publicly_accessible = db.get('PubliclyAccessible', False)
        if publicly_accessible:
            results.append({
                'DBInstanceIdentifier': db['DBInstanceIdentifier'],
                'Engine': db['Engine'],
                'PubliclyAccessible': True
            })

    return results
