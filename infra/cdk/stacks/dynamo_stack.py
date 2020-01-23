from aws_cdk import (
    core,
    aws_dynamodb as ddb,
    aws_dynamodb_global as ddbg,
    aws_iam as iam
)

from stacks.lib.global_table_encrypter import GlobalTableEncrypter


class DynamoStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        player_table_name = 'Players'

        global_table = ddbg.GlobalTable(
            self, 'Players',
            regions=['us-east-1', 'us-east-2'],
            partition_key={'name': 'path', 'type': ddb.AttributeType.STRING},
            table_name=player_table_name
        )

        regions = ['us-east-1', 'us-east-2']

        lambda_global_table_encrypter = GlobalTableEncrypter(
            self, id, regions, player_table_name
        )

        lambda_global_table_encrypter.add_dependency(self)

