# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from cfnlint.rules import CloudFormationLintRule
from cfnlint.rules import RuleMatch


class AMSResourceUnsupportedAttributes(CloudFormationLintRule):
    """Check Base Resource Configuration"""

    id = "E3094"
    shortdesc = "Check for unsupported resource attributes"
    description = "Verify that resource attributes are supported by AMS"
    source_url = "https://aws.amazon.com/managed-services/features"
    tags = ["resources", "attributes", "support", "AMS"]

    def match(self, cfn):
        """Check CloudFormation Resources"""

        matches = []

        invalid_resource_attributes = {
            "AWS::SecretsManager::Secret": ["SecretString"],
            "AWS::DMS::Endpoint": ["MongoDbSettings"],
            "AWS::EC2::LaunchTemplate": ["KeyName"]
        }

        for resource_name, resource_values in cfn.template.get("Resources", {}).items():
            self.logger.debug("Validating Properties for %s resource", resource_name)

            resource_type = resource_values.get("Type", "")

            if resource_type in invalid_resource_attributes.keys():
                check_attributes = set(invalid_resource_attributes[resource_type])

                for attribute, _ in resource_values["Properties"].items():
                    if attribute in check_attributes:
                        message = "AMS - Attribute {0} for resource {1} is not supported by AMS"
                        matches.append(
                            RuleMatch(
                                ["Resources", resource_name, attribute],
                                message.format(attribute, resource_name),
                            )
                        )

        return matches
