# Automated AWS EC2 Scheduler (Cost Saver)

##  Project Overview
This project implements an automated "FinOps" solution to reduce AWS cloud costs. It automatically stops non-production EC2 instances outside of business hours (8 PM IST) and starts them before the workday begins (9 AM IST).

For a standard t2.micro instance or larger development servers, this reduces running hours from 168 hours/week to approx 55 hours/week, potentially saving ~65% on compute costs.

##  Architecture
The solution uses a Serverless architecture to minimize maintenance overhead:

Amazon EventBridge (Scheduler): triggers the workflow on a Cron schedule.

AWS Lambda (Python 3.9): executes the business logic using the boto3 SDK.

AWS IAM: ensures "Least Privilege" access control (Lambda can only start/stop instances, not terminate them).

Amazon EC2 (Target): The instances are identified via Resource Tagging (Env: Dev).

##  How It Works
Tagging: The script scans the region for EC2 instances with the tag Env=Dev.

Filtering: It isolates the instance IDs that match the criteria.

Action: Depending on the event payload ({"action": "stop"} or {"action": "start"}), it toggles the instance state.

## Setup Instructions
Prerequisites
AWS Account with permissions to create Lambda functions and IAM Roles.

Python 3 installed locally for testing.

Deployment Steps
Create IAM Role:

Trusted Entity: Lambda

Permissions: AmazonEC2FullAccess (Restricted to specific resources in Prod), AWSLambdaBasicExecutionRole.

Deploy Lambda:

Runtime: Python 3.9

Copy code from lambda_function.py

Set Timeout to 10 seconds.

Configure EventBridge:

Stop Rule: Cron 30 14 * * ? * (14:30 UTC = 8:00 PM IST) -> Input: {"action": "stop"}

Start Rule: Cron 30 03 * * ? * (03:30 UTC = 9:00 AM IST) -> Input: {"action": "start"

Code Example
The core logic utilizes boto3 to filter instances:
```
filters = [{
    'Name': 'tag:Env',
    'Values': ['Dev']
}]
response = ec2.describe_instances(Filters=filters)

```
