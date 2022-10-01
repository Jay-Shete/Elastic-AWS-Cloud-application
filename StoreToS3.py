import os

import boto3

import CommonCredentials


def storeToS3InputBucket(image_name):
    s3_client = boto3.resource("s3", region_name=CommonCredentials.AWS_REGION,
                               aws_access_key_id=CommonCredentials.AWS_ACCESS_KEY,
                               aws_secret_access_key=CommonCredentials.AWS_SECRET_ACCESS_KEY)
    input_bucket = s3_client.Bucket(CommonCredentials.S3_INPUT_BUCKET)

    try:
        file_name = str(image_name)
        input_obj = input_bucket.Object(file_name)
        with open(str(image_name), 'rb') as data:
            input_obj.upload_fileobj(data)
    except Exception as e:
        print(f"File upload to S3 Input Bucket : Fail ::: {repr(e)}")

    print("File upload to S3 Input Bucket : Success")


def storeToS3OutputBucket(name, image_name):
    s3_client = boto3.resource("s3", region_name=CommonCredentials.AWS_REGION,
                               aws_access_key_id=CommonCredentials.AWS_ACCESS_KEY,
                               aws_secret_access_key=CommonCredentials.AWS_SECRET_ACCESS_KEY)
    output_bucket = s3_client.Bucket(CommonCredentials.S3_OUTPUT_BUCKET)
    file_name = str(image_name).split(".")[0]
    output_obj = output_bucket.Object(file_name)
    formatted_output = file_name + ', ' + name
    output_bucket_response = output_obj.put(Body=formatted_output)

    if output_bucket_response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("File upload to S3 Output Bucket : Success")
    else:
        print("File upload to S3 Output Bucket : Fail")

    os.system("rm " + str(image_name))


