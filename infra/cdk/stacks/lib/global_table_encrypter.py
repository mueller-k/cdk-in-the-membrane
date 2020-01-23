from aws_cdk import (
    core,
    aws_cloudformation as cfn,
    aws_iam as iam,
    aws_lambda as lambduh
)
import os
from pathlib import Path

class GlobalTableEncrypter(core.Stack):

    def __init__(self, scope: core.Construct, id: str, regions: list, table_name: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)


        root_dir = Path(os.path.realpath(__file__)).parent.parent.parent.parent.parent

        lambdaFunction = lambduh.SingletonFunction(
            self,
            'SingletonLambda',
            code=lambduh.Code.asset(os.path.join(root_dir, 'src', 'lambda')),
            description='Lambda to update DynamoDB global table sse spec with customer managed KMS key',
            handler='sse_spec_ddbg.handler',
            runtime=lambduh.Runtime.NODEJS_10_X,
            timeout=core.Duration.minutes(15),
            uuid='15a28fa7-2a1e-4c3b-b514-2f58c0ee19ed'
        )

        customResource = cfn.CustomResource(
            self,
            'CfnCustomResource',
            provider=cfn.CustomResourceProvider.from_lambda(lambdaFunction),
            properties={
                'regions':regions,
                'resourceType':'Custom::DynamoGlobalTableEncrypter',
                'tableName':table_name
            },
            removal_policy=core.RemovalPolicy.RETAIN
        )

def grantUpdateGlobalTableLambda(principal: iam.IPrincipal):
    principal.add_to_policy(iam.PolicyStatement(
        resources=['*'],
        actions=[
            "iam:CreateServiceLinkedRole",
            "application-autoscaling:DeleteScalingPolicy",
            "application-autoscaling:DeregisterScalableTarget",
            "dynamodb:CreateGlobalTable", "dynamodb:DescribeLimits",
            "dynamodb:DeleteTable", "dynamodb:DescribeGlobalTable",
            "dynamodb:UpdateGlobalTable",
        ]
    ))
