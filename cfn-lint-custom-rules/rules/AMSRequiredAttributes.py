# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from cfnlint.rules import CloudFormationLintRule
from cfnlint.rules import RuleMatch


class AMSRequiredAttributes(CloudFormationLintRule):
    """Check Base Resource Configuration"""

    id = "E3098"
    shortdesc = "Verify attributes"
    description = "Verify that resource attributes are in format required by AMS"
    source_url = "https://aws.amazon.com/managed-services/features"
    tags = ["resources", "attributes", "format", "support", "ams"]

    def match(self, cfn):
        """Check CloudFormation Resources"""

        matches = []
        required_attributes = {"AWS::Elasticsearch::Domain": ["VPCOptions"]}

        for resource_name, resource_values in cfn.template.get("Resources", {}).items():

            self.logger.debug("Validating Properties for %s resource", resource_name)

            matched = False
            resource_type = resource_values.get("Type", "")

            if resource_type in required_attributes.keys():
                check_attributes = required_attributes[resource_type]
                resource_attributes = set(
                    [attribute for attribute, _ in resource_values["Properties"].items()]
                )

                for attribute in check_attributes:
                    if attribute not in resource_attributes:
                        matched = True
                        break

                if matched:
                    message = "AMS - Resource {} missing one of required property attributes: {}."
                    matches.append(
                        RuleMatch(
                            ["Resources", resource_name],
                            message.format(resource_type, check_attributes),
                        )
                    )

        return matches
