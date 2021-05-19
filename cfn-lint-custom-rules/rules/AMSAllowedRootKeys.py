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
