AWS_REGION = "us-east-1"

AWS_ACCESS_KEY = "AKIA3WXKMVVL34UJMUWD"
AWS_SECRET_ACCESS_KEY = "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"

MESSAGE_ATTRIBUTES = ['ImageName', 'UID']

INPUT_FROM_WebTierToAppTierQueue = "https://sqs.us-east-1.amazonaws.com/804724190551/WebTierToAppTierSQS"
INPUT_FROM_AppTierToWebTierQueue = "https://sqs.us-east-1.amazonaws.com/804724190551/AppTierToWebTierSQS"

S3_INPUT_BUCKET="inputbuckettrinity"
S3_OUTPUT_BUCKET="outputbuckettrinity"

user_data = ''''''

#AMI_ID='ami-08374233d73cf5823'
#AMI_ID='ami-0d965e82f0fbb1f8f'
AMI_ID='ami-0d9380f7169894239'
#AMI_ID='ami-0bb1040fdb5a076bc'
SECURITY_GROUP_ID='sg-083d7e40863a6a706'
