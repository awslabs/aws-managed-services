# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from cfnlint.rules import CloudFormationLintRule
from cfnlint.rules import RuleMatch

class AMSAllowedRootKeys(CloudFormationLintRule):
    """Check Base Template Settings"""

    id = "E1099"
    shortdesc = "Approved AMS CloudFormation top-level template keys"
    description = "Ensure that only AMS approved top-level template keys are used"
    source_url = "https://aws.amazon.com/managed-services/features"
    tags = ["approved", "root", "keys"]

    required_keys = set(
        [
            "AWSTemplateFormatVersion",
            "Description",
            "Mappings",
            "Parameters",
            "Conditions",
            "Resources",
            "Outputs",
            "Metadata",
        ]
    )

    def match(self, cfn):
        """AMS Supported Root Keys Matching"""
        matches = []

        top_level = [section for section in cfn.template]

        for section in top_level:
            if section not in self.required_keys:
                message = "AMS - Top level item {0} not supported by AMS"
                matches.append(RuleMatch([section], message.format(section)))

        return matches
