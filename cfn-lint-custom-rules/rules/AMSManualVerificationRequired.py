# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

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
