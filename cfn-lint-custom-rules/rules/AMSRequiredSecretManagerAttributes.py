"""
  Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.

  Permission is hereby granted, free of charge, to any person obtaining a copy of this
  software and associated documentation files (the "Software"), to deal in the Software
  without restriction, including without limitation the rights to use, copy, modify,
  merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
  permit persons to whom the Software is furnished to do so.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
  PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from cfnlint.rules import CloudFormationLintRule
from cfnlint.rules import RuleMatch


class AMSRequiredSecretManagerAttributes(CloudFormationLintRule):
    """Check Base Resource Configuration"""

    id = "E3096"
    shortdesc = "Check that resource attributes are using Secrets Manager"
    description = "Verify that resource attributes are using Secrets Manager - required by AMS"
    source_url = "https://aws.amazon.com/managed-services/features"
    tags = ["resources", "attributes", "secrets", "manager", "support", "AMS"]

    def match(self, cfn):
        """Check CloudFormation Resources"""

        matches = []

        resources_require_secrets_manager = {
            "AWS::RDS::DBInstance": ["MasterUserPassword", "TdeCredentialPassword"],
            "AWS::RDS::DBCluster": ["MasterUserPassword"],
            "AWS::ElastiCache::ReplicationGroup": ["AuthToken"],
            "AWS::DMS::Certificate": ["CertificatePem", "CertificateWallet"],
            "AWS::DMS::Endpoint": ["Password"],
            "AWS::DocDB::DBCluster": ["MasterUserPassword"],
            "AWS::CodePipeline::Webhook": ["SecretToken"],
        }

        for resource_name, resource_values in cfn.template.get("Resources", {}).items():
            self.logger.debug("Validating Properties for %s resource", resource_name)

            resource_type = resource_values.get("Type", "")

            if resource_type in resources_require_secrets_manager.keys():
                check_attributes = set(resources_require_secrets_manager[resource_type])

                for attribute, attribute_property in resource_values["Properties"].items():
                    if attribute in check_attributes and any(
                        [
                            not isinstance(attribute_property, str),
                            not attribute_property.startswith(
                                ("{{resolve:secretsmanager:", "{{resolve:ssm-secure:")
                            ),
                            not attribute_property.endswith("}}"),
                        ]
                    ):
                        # noqa: E501
                        message = "AMS - Property {0} is only allowed with Secrets Manager/Systems Manager Parameter Store(Secure String Parameter)"
                        matches.append(
                            RuleMatch(
                                ["Resources", resource_name, attribute], message.format(attribute)
                            )
                        )

        return matches
