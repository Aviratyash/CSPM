import json
from inventory.ec2 import list_ec2_instances
from inventory.s3 import list_s3_buckets
from checks.s3_public import check_public_buckets
from inventory.iam import list_iam_users
from checks.security_groups import check_open_security_groups
from checks.iam_mfa import check_iam_users_without_mfa
from checks.iam_wildcard_roles import check_iam_roles_with_wildcards
from checks.rds_public import check_public_rds_instances
from checks.lambda_permissions import check_lambda_roles_with_wildcards
from reports.html_reports import generate_html_report
from checks.iam_unused import check_unused_iam_entities
from checks.s3_encryption import check_s3_encryption_disabled
from slack_alert import send_slack_alert

def run_inventory():
    inventory_data = {
        'EC2': list_ec2_instances(),
        'S3': list_s3_buckets(),
        'IAM': list_iam_users()
    }

    misconfig_data = {
    'PublicS3Buckets': check_public_buckets(),
    'OpenSecurityGroups': check_open_security_groups(),
    'IAMUsersWithoutMFA': check_iam_users_without_mfa(),
    'IAMRolesWithWildcards': check_iam_roles_with_wildcards(),
    'PublicRDSInstances': check_public_rds_instances(),
    'LambdaWidePermissions': check_lambda_roles_with_wildcards(),
    'S3EncryptionDisabled': check_s3_encryption_disabled(),
    'IAMUnusedEntities': check_unused_iam_entities(),


}
    SLACK_WEBHOOK = "https://hooks.slack.com/services/......"  # replace with your actual webhook URL

    for section, items in misconfig_data.items():
        for item in items:
            if item.get("Severity") == "High":
                message = f"🚨 [High] {section} issue found:\n{item}"
                send_slack_alert(message, SLACK_WEBHOOK)


    report = {
        'Inventory': inventory_data,
        'Misconfigurations': misconfig_data
    }

    with open("reports/inventory.json", "w") as f:
        json.dump(report, f, indent=4)

    print("✅ Inventory + Misconfiguration check completed.")
    generate_html_report("reports/inventory.json", "reports/report.html")
    print("Report generated Successfully")





if __name__ == "__main__":
    run_inventory()


