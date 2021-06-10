# ams-cfn-lint-custom-rules

CFN Lint custom rules to validate CFN templates for ingestion into AWS Managed Services (AMS). The rules are used in combination with [CloudFormation Linter package](https://github.com/aws-cloudformation/cfn-python-lint) and will help you determine if your custom CloudFormation template can be ingested into an AMS managed account (using AMS Advanced).

## How to use it

1. Install AWS CloudFormation Linter using the instructions [here](https://github.com/aws-cloudformation/cfn-lint#aws-cloudformation-linter).
2. Download the rules folder in this repository and remember the path for next step.
3. Run as `cfn-lint --template your_template.yaml --append-rules your_directory_with_custom_rules`.
