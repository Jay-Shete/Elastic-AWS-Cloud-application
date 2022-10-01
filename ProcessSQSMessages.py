import base64
import os
from io import BytesIO
from PIL import Image
import StoreToS3
from ImageRecognition import IdentifyImage


def process_SQS_To_WebTier_message(message):
    print(f"Message Body : {message['Body']}")
    print(f"Message ID : {message['MessageId']}")

    image_name = "default"
    label = ''.join(filter(str.isalnum, str(message['Body'])))

    if message['MessageAttributes'] is not None:
        image_name = message['MessageAttributes']['ImageName']['StringValue']
        uid = message['MessageAttributes']['UID']['StringValue']
        print(f"Image Name : {image_name}")
        print(f"UID : {uid}")

    # with open("result.txt", "a") as file:
    #     file.write( image_name+":"+label)
    #     file.write("\n")

    with open(uid + ".txt", "w") as file:
        file.write(label)


def process_SQS_To_AppTier_message(message):
    print(f"message id: {message['MessageId']}")

    image_name = "default"
    uid = "default"

    if message['MessageAttributes'] is not None:
        image_name = message['MessageAttributes']['ImageName']['StringValue']
        uid = message['MessageAttributes']['UID']['StringValue']
        print("Image Name: ", image_name)
        print("UID: ", uid)

    # Save Image
    im2 = base64.b64decode(message['Body'])
    with open(image_name, "wb") as f:
        f.write(im2)

    if not os.path.exists(image_name):
        im = Image.open(BytesIO(base64.b64decode(message['Body'])))
        im.save(image_name)

    output = IdentifyImage(image_name)
    name = output if output else 'default'

    print(name)

    StoreToS3.storeToS3InputBucket(image_name)

    StoreToS3.storeToS3OutputBucket(name, image_name)

    result = {
        'ImageName': image_name,
        'Name': name,
        'UID': uid
    }

    return result
