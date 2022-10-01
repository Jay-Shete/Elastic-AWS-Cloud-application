from datetime import datetime

from ProcessSQSMessages import process_SQS_To_AppTier_message
import CommonCredentials
from SQSOperations import ReceiveMsgFromSQS, DeleteMsgFromSQS, SendMessageFromAppTierToSQS

if __name__ == "__main__":

    # receive_message() from queue
    while True:
        response = ReceiveMsgFromSQS(CommonCredentials.INPUT_FROM_WebTierToAppTierQueue)

        if 'Messages' in response:
            for message in response['Messages']:
                try:
                    print("============================")
                    print("Message received at : ", datetime.now())  # .strftime("%H:%M:%S")
                    result = process_SQS_To_AppTier_message(message)
                    print("============================")
                except Exception as e:
                    print(f"Exception in appTier - processing message: {repr(e)}")
                    continue

                try:
                    SendMessageFromAppTierToSQS(result, CommonCredentials.INPUT_FROM_AppTierToWebTierQueue)
                    print("============================")
                except Exception as e:
                    print(f"Exception in appTier - sending message: {repr(e)}")
                    continue

                try:
                    receipt_handle = message['ReceiptHandle']
                    DeleteMsgFromSQS(CommonCredentials.INPUT_FROM_WebTierToAppTierQueue, receipt_handle)
                except Exception as e:
                    print(f"Exception in appTier - deleting message: {repr(e)}")
                    continue
