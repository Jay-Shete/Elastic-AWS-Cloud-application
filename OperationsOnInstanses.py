import math
import time

from CommonCredentials import INPUT_FROM_WebTierToAppTierQueue, AMI_ID, user_data, SECURITY_GROUP_ID, \
    INPUT_FROM_AppTierToWebTierQueue


def find_instances(ec2resource, values):
    instances = ec2resource.instances.filter(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': values
            },
            {
                'Name': 'tag:Type',
                'Values': ['apptier']
            }
        ]
    )

    instances_count = 0
    for x in instances:
        instances_count += 1
    return instances_count


def get_required_instance_count(sqsclient):
    print("Entered get_required_instance_count")
    response = sqsclient.get_queue_attributes(
        QueueUrl=INPUT_FROM_WebTierToAppTierQueue,
        AttributeNames=['ApproximateNumberOfMessages', 'ApproximateNumberOfMessagesNotVisible',
                        'ApproximateNumberOfMessagesDelayed']
    )

    queue_size = int(response['Attributes']['ApproximateNumberOfMessages']) + int(
        response['Attributes']['ApproximateNumberOfMessagesNotVisible'])
    print("Current queue size : " + str(queue_size))

    required_instances_to_create = math.ceil(queue_size / 2)
    required_instances_to_terminate = math.ceil(queue_size / 10)

    return required_instances_to_create, required_instances_to_terminate


def create_apptier_instances(ec2resource, requiredInstances, no_Of_Current_Instances):
    print("Entered create_apptier_instances()")
    i = 0
    while i < requiredInstances and no_Of_Current_Instances <= 10:
        no_Of_Current_Instances += 1

        instance_name = 'app-instance-' + str(no_Of_Current_Instances)
        print("Creating ", instance_name)

        ec2resource.create_instances(
            ImageId=AMI_ID,
            InstanceType='t2.micro',
            UserData=user_data,
            MinCount=1, MaxCount=1,
            SecurityGroupIds=[
                SECURITY_GROUP_ID,
            ],
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': instance_name
                        },
                        {
                            'Key': 'Type',
                            'Value': 'apptier'
                        }
                    ]
                },
            ])

        i += 1

    time.sleep(30)
    return no_Of_Current_Instances


def terminate_apptier_instances(ec2resource, instances_to_be_terminated, no_Of_Current_Instances):
    print("Entered terminate_apptier_instances()")
    i = 0

    while (i < instances_to_be_terminated):
        appname = "app-instance-" + str(no_Of_Current_Instances)

        instance_list = ec2resource.instances.filter(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': [appname]
                },
                {
                    'Name': 'instance-state-name',
                    'Values': ['running', 'pending']
                }
            ]
        )

        for each in instance_list:
            curr_instance = ec2resource.Instance(each.id)
            curr_instance.terminate()

        no_Of_Current_Instances -= 1
        i += 1

        print("Terminated " + appname)

        return no_Of_Current_Instances

def getWebTierToSQSCount(sqsClient):
    response = sqsClient.get_queue_attributes(
        QueueUrl=INPUT_FROM_WebTierToAppTierQueue,
        AttributeNames=['ApproximateNumberOfMessages', 'ApproximateNumberOfMessagesNotVisible',
                        'ApproximateNumberOfMessagesDelayed']
    )

    queue_size = int(response['Attributes']['ApproximateNumberOfMessages']) + int(
        response['Attributes']['ApproximateNumberOfMessagesNotVisible'])
    print("WebTier to SQS queue size : " + str(queue_size))
    return queue_size;

def getSQSToWebTierCount(sqsClient):
    response = sqsClient.get_queue_attributes(
        QueueUrl=INPUT_FROM_AppTierToWebTierQueue,
        AttributeNames=['ApproximateNumberOfMessages', 'ApproximateNumberOfMessagesNotVisible',
                        'ApproximateNumberOfMessagesDelayed']
    )

    queue_size = int(response['Attributes']['ApproximateNumberOfMessages']) + int(
        response['Attributes']['ApproximateNumberOfMessagesNotVisible'])
    print("SQS to webTier queue size : " + str(queue_size))
    return queue_size;