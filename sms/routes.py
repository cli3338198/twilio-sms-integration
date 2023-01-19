from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse
from nums_api.sms.api import get_random_fact

sms = Blueprint('sms', __name__)


@sms.route('/', methods=["GET", "POST"])
def sms_reply():
  """
  Reply to a SMS with a random fact. 

  Requires the word 'fact' in the text message to respond with a fact otherwise
  responds with "Please respond with the word 'Fact'.".

  Input:
      body (str) - the texted string
  Output:
      MessagingResponse (str) - serialized XML like Twilio markup language
                                used to build your SMS

        <?xml version="1.0" encoding="UTF-8"?>
        <Response>
            <Say>Thanks for calling!</Say>
        </Response>

  """

  body = request.values.get('Body', None)
  resp = MessagingResponse()

  if not body or 'fact' not in body.lower():

    resp.message("Please respond with the word 'Fact'.")
    return str(resp)


  random_fact = get_random_fact()
  
  resp.message(random_fact)
  return str(resp)
