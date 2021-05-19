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
