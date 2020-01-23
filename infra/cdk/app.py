#!/usr/bin/env python3

from aws_cdk import core

from stacks.dynamo_stack import DynamoStack


APP = core.App()
DynamoStack(APP, "cdk-in-the-membrane", env={'region': 'us-east-1'})

APP.synth()
