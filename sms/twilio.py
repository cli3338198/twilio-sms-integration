import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
MESSENGING_SERVICE_SID = os.environ['MESSENGING_SERVICE_SID']

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_sms(body, to):
  """
  Send a sms message. 

  USE ONLY FOR TESTING PURPOSES.

  Input:  
      body (str)
      to (str) - a phone number, eg. +18007686789
  
  """

  message = client.messages \
                .create(
                     body=body,
                     messaging_service_sid=MESSENGING_SERVICE_SID,
                     to=to
                 )

  print(message.sid)