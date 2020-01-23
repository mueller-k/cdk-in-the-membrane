import json
import pytest

from aws_cdk import core
from cdk-in-the-membrane.cdk_in_the_membrane_stack import CdkInTheMembraneStack


def get_template():
    app = core.App()
    CdkInTheMembraneStack(app, "cdk-in-the-membrane")
    return json.dumps(app.synth().get_stack("cdk-in-the-membrane").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
