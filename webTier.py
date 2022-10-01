import os
import boto3
from flask import Flask, request
import base64
import uuid
from datetime import datetime

app = Flask(__name__)

AWS_REGION = "us-east-1"

AWS_ACCESS_KEY="AKIA3WXKMVVL34UJMUWD"
AWS_SECRET_ACCESS_KEY="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"
sqs_client = boto3.client("sqs", region_name=AWS_REGION)

session=boto3.session.Session()
sqs_resource = session.resource("sqs",region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

INPUT_QUEUE_URL="https://sqs.us-east-1.amazonaws.com/804724190551/WebTierToAppTierSQS"
INPUT_QUEUE_NAME="WebTierToAppTierSQS"

@app.route("/")
def print_hi():
    return "<p>Hello Flask Server</p>"


@app.route("/", methods=['POST'])
def readImageFile():
    WebToAppTierQueue = sqs_resource.get_queue_by_name(QueueName=INPUT_QUEUE_NAME)

    FileRecievedFromWorkloadGenerator = request.files['myfile']

    if FileRecievedFromWorkloadGenerator.filename!= '':
        FileRecievedFromWorkloadGenerator.save(FileRecievedFromWorkloadGenerator.filename)

        with open(FileRecievedFromWorkloadGenerator.filename, "rb") as image_file:
            image_file_converted_to_encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            image_file.close()

        msg_uuid = str(uuid.uuid4())

        try:
            WebToAppTierQueue.send_message(MessageBody=image_file_converted_to_encoded_string, MessageAttributes={
                'ImageName': {
                    'StringValue': FileRecievedFromWorkloadGenerator.filename,
                    'DataType': 'String'
                },
                'UID': {
                    'StringValue': msg_uuid,
                    'DataType': 'String'
                }
            })

        except Exception as e:
            print(f"Exception while sending message to SQS ::: " + FileRecievedFromWorkloadGenerator.filename + " ::: {repr(e)}")

        print("Message sent for " + FileRecievedFromWorkloadGenerator.filename + " at : ",datetime.now()) #.strftime("%H:%M:%S")

    result = None

    while result is None:
        if os.path.exists(msg_uuid + ".txt"):
            with open(msg_uuid + ".txt") as file:
                result = file.read()
                print("Result for " + FileRecievedFromWorkloadGenerator.filename + " : ", result)
                if result:
                    os.system("rm " + msg_uuid + ".txt")
                    return "For "+FileRecievedFromWorkloadGenerator.filename+": "+str(result)

    print("Exiting...")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
