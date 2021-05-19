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


class AMSResourceSupported(CloudFormationLintRule):
    """Check Base Resource Configuration"""

    id = "E3095"
    shortdesc = "Verify that resources are supported by AMS"
    description = "Verify that resources are supported by AMS"
    source_url = "https://aws.amazon.com/managed-services/features"
    tags = ["resources", "support", "AMS"]

    def match(self, cfn):
        """Check CloudFormation Resources"""

        matches = []
        resources_to_check = []

        valid_resource_types = [
            'AmazonMQ::*',
            'ApiGateway::*',
            'Athena::*',
            'ApplicationAutoScaling::*',
            'AutoScaling::AutoScalingGroup',
            'AutoScaling::LaunchConfiguration',
            'AutoScaling::LifecycleHook',
            'AutoScaling::ScalingPolicy',
            'AutoScaling::ScheduledAction',
            'CertificateManager::*',
            'CloudFormation::CustomResource',
            'CloudFormation::Designer',
            'CloudFormation::WaitCondition',
            'CloudFormation::WaitConditionHandle',
            'CloudFront::CloudFrontOriginAccessIdentity',
            'CloudFront::Distribution',
            'CloudFront::StreamingDistribution',
            'CloudWatch::*',
            'CodeBuild::*',
            'CodeCommit::*',
            'CodeDeploy::*',
            'CodePipeline::*',
            'Cognito::*',
            'Custom::*',
            'DMS::Certificate',
            'DMS::Endpoint',
            'DMS::EventSubscription',
            'DMS::ReplicationInstance',
            'DMS::ReplicationSubnetGroup',
            'DMS::ReplicationTask',
            'DocDB::*',
            'DynamoDB::*',
            'EC2::EIP',
            'EC2::EIPAssociation',
            'EC2::Host',
            'EC2::Instance',
            'EC2::LaunchTemplate',
            'EC2::NetworkInterface',
            'EC2::NetworkInterfaceAttachment',
            'EC2::SecurityGroup',
            'EC2::SecurityGroupEgress',
            'EC2::SecurityGroupIngress',
            'EC2::Volume',
            'EC2::VolumeAttachment',
            'ECR::*',
            'ECS::*',
            'EFS::FileSystem',
            'EFS::MountTarget',
            'ElastiCache::*',
            'ElasticLoadBalancing::LoadBalancer',
            'ElasticLoadBalancingV2::Listener',
            'ElasticLoadBalancingV2::ListenerCertificate',
            'ElasticLoadBalancingV2::ListenerRule',
            'ElasticLoadBalancingV2::LoadBalancer',
            'ElasticLoadBalancingV2::TargetGroup',
            'Elasticsearch::*',
            'Events::*',
            'FSx::*',
            'Glue::*',
            'Inspector::*',
            'KMS::Alias',
            'KMS::Key',
            'Kinesis::*',
            'KinesisAnalytics::*',
            'KinesisFirehose::*',
            'LakeFormation::*',
            'Lambda::*',
            'Logs::LogGroup',
            'Logs::LogStream',
            'Logs::MetricFilter',
            'Logs::SubscriptionFilter',
            'MediaConvert::*',
            'MediaStore::*',
            'RDS::DBCluster',
            'RDS::DBClusterParameterGroup',
            'RDS::DBInstance',
            'RDS::DBParameterGroup',
            'RDS::DBSubnetGroup',
            'RDS::EventSubscription',
            'RDS::OptionGroup',
            'Redshift::Cluster',
            'Redshift::ClusterParameterGroup',
            'Redshift::ClusterSubnetGroup',
            'Route53::*',
            'S3::Bucket',
            'S3::BucketPolicy',
            'SageMaker::*',
            'SDB::*',
            'SES::*',
            'SNS::*',
            'SQS::Queue',
            'SQS::QueuePolicy',
            'SSM::Parameter',
            'SecretsManager::*',
            'SecurityHub::*',
            'StepFunctions::*',
            'Transfer::*',
            'WAF::*',
            'WAFRegional::*',
            'WAFv2::*',
            'WorkSpaces::*']

        resources = cfn.get_resources()

        for resource_name, resource_values in resources.items():

            path = ["Resources", resource_name]

            if "Type" not in resource_values:
                message = "AMS - {0} Type key is missing"
                matches.append(RuleMatch(path, message.format("/".join(map(str, path)))))
                continue

            self.logger.debug("Validating %s as supported by AMS", resource_name)

            resources_to_check.append(resource_values.get("Type").replace('AWS::', ''))

            if valid_resource_types or resources_to_check:
                resources = set(resources_to_check) - set(valid_resource_types)

                if resources:
                    for resource in resources:
                        if ((resource.split("::"))[0]) + \
                                "::*" not in valid_resource_types and resources not in valid_resource_types:
                            message = "AMS - {0} Resource not supported"
                            matches.append(RuleMatch(path, message.format("/".join(map(str, path)))))

        # Patch system does not support combinations of EC2+ASG
        if "EC2::Instance" in resources_to_check and "AutoScaling::AutoScalingGroup" in resources_to_check:
            # noqa: E501
            message = "AMS - Resources 'AWS::EC2::Instance' and 'AWS::AutoScaling::AutoScalingGroup' are not supported in the same stack by the AMS Patch system"
            matches.append(RuleMatch(path, message))

        return matches
