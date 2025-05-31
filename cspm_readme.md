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
├── main.py                 # Main execution script
├── checks/
│   ├── __init__.py
│   ├── iam_checks.py       # IAM-related security checks
│   ├── s3_checks.py        # S3 bucket encryption checks
│   ├── rds_checks.py       # RDS exposure checks
│   └── lambda_checks.py    # Lambda permission checks
│
├── slack_alert.py          # Slack webhook integration
├── report_generator.py     # HTML report generation
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore
└── README.md              # This file
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
   # Copy .env.example to .env
   cp .env.example .env
   
   # Edit .env file and add your webhook URL
   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/your/webhook/url
   ```

---

## 🚀 Usage

### Basic Scan
```bash
python main.py
```

### Advanced Options
```bash
# Scan specific services only
python main.py --services iam,s3

# Skip Slack notifications
python main.py --no-slack

# Custom output directory
python main.py --output-dir ./custom-reports
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
- 🔧 Step-by-step remediation instructions
- 📊 Visual risk assessment charts
- 🕒 Timestamp and scan metadata

Report location: `./reports/security_report_YYYY-MM-DD_HH-MM-SS.html`

---

## 🧪 Testing

### Test Slack Integration
```bash
# Run test mode to verify Slack webhook
python main.py --test-slack
```

### Simulate High-Severity Finding
Create a test IAM user without MFA to trigger alerts:
```bash
aws iam create-user --user-name test-user-no-mfa
```

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

### Adding New Security Checks

1. Create a new check file in the `checks/` directory
2. Implement your check function following this pattern:

```python
def check_new_service(session):
    """
    Check for security misconfigurations in New Service
    
    Args:
        session: boto3 session object
        
    Returns:
        list: List of finding dictionaries
    """
    findings = []
    client = session.client('newservice')
    
    # Your check logic here
    
    return findings
```

3. Import and register in `main.py`

### Customizing Risk Scores

Edit the risk scoring logic in individual check files:

```python
# Example: Adjust risk score based on resource criticality
risk_score = 8 if is_production_resource else 5
```

---

## 🚦 Roadmap

- [ ] **Multi-cloud Support**
  - Azure security assessments
  - Google Cloud Platform checks
  
- [ ] **Advanced Features**
  - Auto-remediation scripts
  - Custom rule engine
  - Historical trend analysis
  
- [ ] **Integrations**  
  - Jira ticket creation
  - PagerDuty integration
  - Splunk/ElasticSearch export

- [ ] **Enterprise Features**
  - Role-based access control
  - Multi-tenant support
  - Compliance framework mapping (SOC2, NIST, etc.)

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linting
flake8 .
black .
```

### Submitting Changes
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 Support

- 📧 **Email**: security-team@yourcompany.com
- 💬 **Slack**: #security-tools
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/cspm-tool/issues)
- 📖 **Documentation**: [Wiki](https://github.com/yourusername/cspm-tool/wiki)

---

## 🙏 Acknowledgments

- AWS SDK for Python (Boto3) team
- Open source security community
- Contributors and testers

---

**⚠️ Disclaimer**: This tool is provided as-is for security assessment purposes. Always test in non-production environments first and ensure you have proper authorization before scanning AWS resources.