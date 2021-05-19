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


class AMSManualVerificationRequired(CloudFormationLintRule):
    """Check Base Resource Configuration"""

    id = "E3099"
    shortdesc = "Check for resources that require manual verification by AMS"
    description = (
        "Check resources that require review/verification from AMS operations/security team"
    )
    source_url = "https://aws.amazon.com/managed-services/features"
    tags = ["resources", "support", "AMS", "review", "verification"]

    def match(self, cfn):
        """Check CloudFormation Resources"""

        matches = []

        resources_requiring_verification = (
            "AWS::S3::BucketPolicy",
            "AWS::SQS::QueuePolicy",
            "AWS::SNS::TopicPolicy",
        )

        resources = cfn.get_resources()

        for resource_name, resource_values in resources.items():
            path = ["Resources", resource_name]
            res_type = resource_values.get("Type")
            self.logger.debug(
                "Checking if %s resource requires manual verification by AMS", resource_name
            )
            if res_type in resources_requiring_verification:
                message = "AMS - Template contains resource {0}. The permissions defined in this resource will be manually validated by the AMS Security Operations team"
                matches.append(RuleMatch(path, message.format("/".join(map(str, path)))))

        return matches
