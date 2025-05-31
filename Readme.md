# 🛡️ Cloud Security Posture Management (CSPM) Tool

A lightweight, Python-based CSPM tool designed to detect common AWS security misconfigurations and send real-time alerts to Slack. Built for security teams who need automated monitoring of cloud infrastructure security posture.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![AWS](https://img.shields.io/badge/AWS-Compatible-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Slack](https://img.shields.io/badge/Slack-Integration-purple.svg)

---

## 🚀 Features

- ✅ **IAM Security Checks**
  - Detects IAM users without MFA enabled
  - Identifies IAM roles with wildcard (`*`) permissions
  - Finds unused IAM users and roles (inactive for >90 days)

- ✅ **Infrastructure Security**
  - Detects RDS instances with public access enabled
  - Identifies S3 buckets without default encryption
  - Analyzes Lambda functions with over-permissive roles

- ✅ **Alerting & Reporting**
  - Real-time **Slack notifications** for high-severity findings
  - Generates comprehensive HTML security reports
  - Risk scoring system (1-10 scale)
  - Detailed remediation guidance

---

## 📁 Project Structure

```
CSPM/
│
├── main.py # Main orchestration script
├── slack_alert.py # Slack integration module
│
├── checks/ # Misconfiguration detection modules
│ ├── iam_mfa.py # IAM users without MFA
│ ├── iam_unused.py # Inactive IAM users/roles
│ ├── iam_wildcard_roles.py # Roles with wildcard permissions
│ ├── lambda_permissions.py # Over-permissive Lambda roles
│ ├── rds_public.py # Publicly accessible RDS instances
│ ├── s3_encryption.py # S3 buckets without encryption
│ ├── s3_public.py # Publicly accessible S3 buckets
│ └── security_groups.py # Overly permissive security groups
│
├── inventory/ # AWS resource fetchers
│ ├── ec2.py
│ ├── iam.py
│ └── s3.py
│
├── reports/ # Report generation
│ ├── html_reports.py # HTML report generator
│ ├── inventory.json # Raw data snapshot (if any)
│ └── report.html # Final HTML report
│
└── README.md
```

---

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/cspm-tool.git
cd cspm-tool
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure AWS Credentials

Ensure your AWS credentials are properly configured:

**Option 1: AWS CLI**
```bash
aws configure
```

**Option 2: Environment Variables**
```bash
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="us-east-1"
```

**Option 3: IAM Roles (Recommended for EC2/Lambda)**
- Attach appropriate IAM role to your compute instance

### 4. Set Up Slack Integration

1. Create a Slack incoming webhook:
   - Go to your Slack workspace settings
   - Navigate to **Apps** → **Incoming Webhooks**
   - Create a new webhook for your desired channel

2. Configure the webhook URL:
   ```bash

   # Edit main.py file and add your webhook URL
   SLACK_WEBHOOK = https://hooks.slack.com/services/your/webhook/url
   ```

---

## 🚀 Usage

### Basic Scan
```bash
python main.py
```

---

## 📊 Sample Output

### Slack Alert Example
```
🚨 [HIGH SEVERITY] Security Misconfiguration Detected

Service: IAM
Issue: User without MFA enabled
Resource: admin-user
Risk Score: 9/10

Recommendation: Enable MFA for this user immediately
AWS Console: IAM → Users → admin-user → Security credentials → MFA
```

### HTML Report Features
- 📈 Executive summary with risk metrics
- 📋 Detailed findings table with severity levels
- 📊 Visual risk assessment charts


Report location: `./reports/report.html`

---

---

## ⚙️ Configuration

### Required AWS Permissions

Your AWS credentials need the following permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "iam:ListUsers",
                "iam:ListRoles",
                "iam:ListMFADevices",
                "iam:GetUser",
                "iam:GetRole",
                "s3:ListAllMyBuckets",
                "s3:GetBucketEncryption",
                "rds:DescribeDBInstances",
                "lambda:ListFunctions",
                "lambda:GetFunction"
            ],
            "Resource": "*"
        }
    ]
}
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SLACK_WEBHOOK_URL` | Slack incoming webhook URL | Yes (for alerts) |
| `AWS_DEFAULT_REGION` | Default AWS region for scanning | No (defaults to us-east-1) |
| `REPORT_OUTPUT_DIR` | Custom directory for HTML reports | No (defaults to ./reports) |
| `HIGH_SEVERITY_THRESHOLD` | Risk score threshold for Slack alerts | No (defaults to 7) |

---

## 🔧 Customization

### 📁 Step 1: Create a New Check File

Navigate to the `checks/` directory and create a new Python file. For example: my_custom.py

Integrate that rule in `main.py` as per the format in tool

Import and register in `main.py`

### Customizing Risk Scores

Edit the risk scoring logic in individual check files:

```python
# Example: Adjust risk score based on resource criticality
risk_score = 8 if is_production_resource else 5
```


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 Support

- 📧 **Email**: yashingole2003@gmail.com

---

## 🙏 Acknowledgments

- AWS SDK for Python (Boto3) team
- Open source security community
- Contributors and testers

---

**⚠️ Disclaimer**: This tool is provided as-is for security assessment purposes. Always test in non-production environments first and ensure you have proper authorization before scanning AWS resources.
