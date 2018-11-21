# Send to single device.
from pyfcm import FCMNotification


# OR initialize with proxies

data_sp = {
          "SpeedValue" : 120
        }
push_service = FCMNotification(api_key="AAAAjRp3LxE:APA91bFXjTalD4MZbZy3QvRj7vQehoYiQgjGkuLopceDW2YooKvrpqiZdEuh6tv2V1P7T6rlsR6lHxBp3CqnlYEX1DrNSnIXFGYWZrwIIBPh6MOLgP_jaZCT3vIdyRfRY_qo-Ev3N6eg")

# Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging


message_title = "OBD Service"
message_body = "Your car has exceeded the speed limit!"
result = push_service.notify_topic_subscribers(topic_name="obdpush", message_title=message_title, message_body=message_body, data_message=data_sp)

print (result)
