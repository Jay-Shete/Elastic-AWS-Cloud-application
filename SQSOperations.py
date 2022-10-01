import boto3

import CommonCredentials


def ReceiveMsgFromSQS(queueURL):
    sqs_client = boto3.client("sqs", region_name=CommonCredentials.AWS_REGION,
                              aws_access_key_id=CommonCredentials.AWS_ACCESS_KEY,
                              aws_secret_access_key=CommonCredentials.AWS_SECRET_ACCESS_KEY)

    response = sqs_client.receive_message(
        QueueUrl=queueURL,
        AttributeNames=CommonCredentials.MESSAGE_ATTRIBUTES,
        MaxNumberOfMessages=10,
        MessageAttributeNames=['All'],
    )
    #print(response)
    return response


def DeleteMsgFromSQS(queueURL,receipt_handle):
    sqs_client = boto3.client("sqs", region_name=CommonCredentials.AWS_REGION,
                              aws_access_key_id=CommonCredentials.AWS_ACCESS_KEY,
                              aws_secret_access_key=CommonCredentials.AWS_SECRET_ACCESS_KEY)

    sqs_client.delete_message(
        QueueUrl=queueURL,
        ReceiptHandle=receipt_handle
    )


def SendMessageFromAppTierToSQS(result, queueURL):
    sqs_client = boto3.client("sqs", region_name=CommonCredentials.AWS_REGION,
                              aws_access_key_id=CommonCredentials.AWS_ACCESS_KEY,
                              aws_secret_access_key=CommonCredentials.AWS_SECRET_ACCESS_KEY)

    sqs_client.send_message(
        QueueUrl=queueURL,
        DelaySeconds=10,
        MessageAttributes={
            'ImageName': {
                'StringValue': result['ImageName'],
                'DataType': 'String'
            },
            'UID': {
                'StringValue': result['UID'],
                'DataType': 'String'
            }
        },
        MessageBody=(result['Name'])
    )