# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

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
