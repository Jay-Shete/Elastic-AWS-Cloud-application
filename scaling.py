import boto3
import time

from CommonCredentials import AWS_REGION, AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY
from OperationsOnInstanses import find_instances, get_required_instance_count, create_apptier_instances, \
    terminate_apptier_instances

sqsclient = boto3.client("sqs",region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
ec2resource = boto3.resource('ec2',region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
idx = -1
tracker=[0,0,0]
no_Of_Current_Instances= 0


while(True):
    no_Of_Current_Instances=find_instances(ec2resource, ['running','pending'])

    required_instances_to_create, required_instances_to_terminate = get_required_instance_count(sqsclient)

    if no_Of_Current_Instances<= 11:
        if(required_instances_to_create > no_Of_Current_Instances):
            RequiredInstances = required_instances_to_create - required_instances_to_terminate
            no_Of_Current_Instances = create_apptier_instances(ec2resource, RequiredInstances,no_Of_Current_Instances)

        elif (required_instances_to_terminate < no_Of_Current_Instances):
            time.sleep(5)
            if idx == 2:
                idx = -1
            idx += 1

            instances_to_be_terminated = abs(required_instances_to_terminate - no_Of_Current_Instances)
            tracker[idx] = instances_to_be_terminated
            print(tracker)
            if tracker.count(instances_to_be_terminated) == 3:
                no_Of_Current_Instances = terminate_apptier_instances(ec2resource,instances_to_be_terminated,no_Of_Current_Instances)

    time.sleep(10)