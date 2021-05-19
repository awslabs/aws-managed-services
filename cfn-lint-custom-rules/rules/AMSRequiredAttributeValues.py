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
import re
from cfnlint.rules import CloudFormationLintRule
from cfnlint.rules import RuleMatch
from cfnlint.helpers import REGEX_DYN_REF


class AMSRequiredAttributeValues(CloudFormationLintRule):
    """Check Base Resource Configuration"""

    id = "E3097"
    shortdesc = "Verify attribute values"
    description = "Verify that resource attribute values are in format required by AMS"
    source_url = "https://aws.amazon.com/managed-services/features"
    tags = ["resources", "attributes", "value", "support", "ams"]

    required_attribute_values = {
        "AWS::EC2::Instance": {
            "IamInstanceProfile": [
                r"customer[^ \n]*",
                r"arn:aws:iam::[\\$\\{AWS::AccountId\\}|[0-9]+:instance-profile\/customer[^ \n]*",
            ]
        },
        "AWS::AutoScaling::LaunchConfiguration": {
            "IamInstanceProfile": [
                r"customer[^ \n]*",
                r"arn:aws:iam::[\\$\\{AWS::AccountId\\}|[0-9]+:instance-profile\/customer[^ \n]*",
            ]
        },
    }

    def match_allowed_values(self, attribute, attribute_value, resource_type):
        """Validate attribute as matching AMS rules


        Arguments:
            attribute {string} -- CloudFormation resource attribute type
            attribute_value {string} -- CloudFormation resource attribute value
            resource_type {string} -- CloudFormation resource type

        """

        check_attributes = set(self.required_attribute_values[resource_type])

        # Don't verify parameters or dynamic references
        if (
            attribute not in check_attributes
            or not isinstance(attribute_value, str)
            or re.match(REGEX_DYN_REF, attribute_value)
        ):
            return True

        for pattern in self.required_attribute_values[resource_type][attribute]:
            p = re.compile(pattern, re.IGNORECASE)
            m = p.match(attribute_value)
            if m:
                return True

        return False

    def match(self, cfn):
        """Check CloudFormation Resources"""

        matches = []

        for resource_name, resource_values in cfn.template.get("Resources", {}).items():
            self.logger.debug("Validating Properties for %s resource", resource_name)

            resource_type = resource_values.get("Type", "")

            if resource_type in self.required_attribute_values.keys():
                for attribute, attribute_value in resource_values["Properties"].items():
                    if not self.match_allowed_values(attribute, attribute_value, resource_type):
                        message = "AMS - Property {0} in {1} does not match with one of: {2}"
                        matches.append(
                            RuleMatch(
                                ["Resources", resource_name, attribute],
                                message.format(
                                    attribute,
                                    resource_values.get("Type", ""),
                                    str(self.required_attribute_values[resource_type][attribute]),
                                ),
                            )
                        )

        return matches
