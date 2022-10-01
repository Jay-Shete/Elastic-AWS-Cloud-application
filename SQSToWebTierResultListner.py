import CommonCredentials
from ProcessSQSMessages import process_SQS_To_WebTier_message
from SQSOperations import ReceiveMsgFromSQS, DeleteMsgFromSQS
from datetime import datetime

if __name__ == "__main__":
    while True:
        response = ReceiveMsgFromSQS(CommonCredentials.INPUT_FROM_AppTierToWebTierQueue)

        if 'Messages' in response:
            for message in response['Messages']:
                try:
                    print("============================")
                    print("Message received at : ", datetime.now())  # .strftime("%H:%M:%S")
                    process_SQS_To_WebTier_message(message)
                    print("============================")
                except Exception as e:
                    print(f"Exception in webTier while reading SQS Queue - processing message: {repr(e)}")
                    continue

                try:
                    receipt_handle = message['ReceiptHandle']
                    DeleteMsgFromSQS(CommonCredentials.INPUT_FROM_AppTierToWebTierQueue,receipt_handle)
                except Exception as e:
                    print(f"Exception in webTier while reading SQS Queue - deleting message: {repr(e)}")
                    continue
