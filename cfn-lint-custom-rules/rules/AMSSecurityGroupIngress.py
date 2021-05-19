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

import ipaddress
from cfnlint.rules import CloudFormationLintRule
from cfnlint.rules import RuleMatch


class SecurityGroupIngress(CloudFormationLintRule):
    """Check EC2 Security Group Ingress Properties"""

    id = "E2599"
    shortdesc = "Verify EC2 Security Group Ingress Properties - AMS"
    description = (
        "Verify EC2 Security Group Ingress Properties as set correctly for AMS requirements"
    )
    source_url = "https://aws.amazon.com/managed-services/features/"
    tags = ["resources", "securitygroup", "ams"]

    allowed_security_group_ingress_rules = [
        {"IpProtocol": "tcp", "FromPort": "80", "ToPort": "80", "AllowAnyIp": True},
        {"IpProtocol": "tcp", "FromPort": "443", "ToPort": "443", "AllowAnyIp": True},
        {"IpProtocol": "6", "FromPort": "80", "ToPort": "80", "AllowAnyIp": True},
        {"IpProtocol": "6", "FromPort": "443", "ToPort": "443", "AllowAnyIp": True},
        {"IpProtocol": "*", "FromPort": "*", "ToPort": "*", "AllowAnyIp": False},
    ]

    # Stores a tuple of CloudFormation resource name and message
    messages = []

    def validate_security_groups(self, resources, allowed_security_group_ingress_rules):
        """Validate security group resources"""

        for resource_name, rblock in resources.items():
            if "SecurityGroupIngress" in rblock["Properties"]:
                rproperties = rblock["Properties"]
                rules = rproperties["SecurityGroupIngress"]
                # Check if a list of ingress rules has been supplied
                if isinstance(rules, list):
                    for rule in rules:
                        self.validate_security_group_rule(
                            rule, allowed_security_group_ingress_rules, resource_name
                        )
                # Else check if an object is supplied - should contain a single ingress rule
                elif isinstance(rules, dict):
                    self.validate_security_group_rule(
                        rules, allowed_security_group_ingress_rules, resource_name
                    )
            elif rblock["Type"] == "AWS::EC2::SecurityGroupIngress":
                rule = rblock["Properties"]
                self.validate_security_group_rule(
                    rule, allowed_security_group_ingress_rules, resource_name
                )

    def validate_security_group_rule(
        self, rule, allowed_security_group_ingress_rules, resource_name
    ):
        """Validate security group rule"""

        for allowed_rule in allowed_security_group_ingress_rules:
            if allowed_rule["IpProtocol"] != "*" and (
                "IpProtocol" in rule and allowed_rule["IpProtocol"] != str(rule["IpProtocol"])
            ):
                """
                If IpProtocol in customer rule does not match with allowed rule"s IpProtocol,
                it means allowed rule is not matching with customer rule and we don't need to check remain properties in the rule.
                """
                continue
            if allowed_rule["FromPort"] != "*" and (
                "FromPort" in rule and allowed_rule["FromPort"] != str(rule["FromPort"])
            ):
                """
                If FromPort in customer rule does not match with allowed rule"s FromPort,
                it means allowed rule is not matching with customer rule and we don't need to check remain properties in the rule.
                """
                continue
            if allowed_rule["ToPort"] != "*" and (
                "ToPort" in rule and allowed_rule["ToPort"] != str(rule["ToPort"])
            ):
                """
                If ToPort in customer rule does not match with allowed rule"s ToPort,
                it means allowed rule is not matching with customer rule and we don't need to check remain properties in the rule.
                """
                continue
            try:
                if (
                    allowed_rule["AllowAnyIp"] is False
                    and "CidrIp" in rule
                    and ipaddress.ip_network(rule["CidrIp"].strip(), False)
                    == ipaddress.ip_network("0.0.0.0/0")
                ):
                    """
                    If there is CidrIp in customer rule and it is 0.0.0.0/0 but AllowAnyIp is False,
                    it means allowed rule is not matching with customer rule.
                    """
                    continue
            except ValueError:
                self.messages.append(
                    (
                        resource_name,
                        "AMS - CidrIp does not represent a valid IPv4 or IPv6 address. \
                        CidrIp value is: %s",
                        rule["CidrIp"].strip(),
                    )
                )
                return
            return

        self.messages.append(
            (
                resource_name,
                "AMS - Invalid SecurityGroup rule found: {0}, violates allowed rules: {1}".format(
                    str(rule), allowed_security_group_ingress_rules
                ),
            )
        )

    def match(self, cfn):
        """Check EC2 Security Group Ingress Resource Parameters - AMS"""

        matches = []
        resources = cfn.get_resources(
            resource_type=("AWS::EC2::SecurityGroup", "AWS::EC2::SecurityGroupIngress")
        )
        self.validate_security_groups(resources, self.allowed_security_group_ingress_rules)

        # Convert rule violations to RuleMatch objects
        for resource_name, message in self.messages:
            path = ["Resources", resource_name]
            matches.append(RuleMatch(path, message))

        return matches
