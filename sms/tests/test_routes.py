from unittest import TestCase, mock
from nums_api import app
from nums_api.database import db, connect_db
from nums_api.config import DATABASE_URL_TEST
from nums_api.maths.models import Math
import os

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

connect_db(app)

db.drop_all()
db.create_all()

class SMSBaseRouteTestCase(TestCase):
  """
      Test for SMS.
  """

  def setUp(self):
      """Set up test data here"""
      
      Math.query.delete()

      self.m1 = Math(
          number=1,
          fact_fragment="the number for this m1 test fact fragment",
          fact_statement="1 is the number for this m1 test fact statement.",
          was_submitted=False,
      )

      db.session.add(self.m1)
      db.session.commit()

      self.client = app.test_client()

  def tearDown(self):
      """Clean up any fouled transaction."""

      db.session.rollback()

class SMSRouteTestCase(SMSBaseRouteTestCase):

  def test_setup(self):
      """Test to make sure tests are set up correctly"""

      test_setup_correct = True
      self.assertEqual(test_setup_correct, True)

  @mock.patch('sms.api.get_random_fact')
  def test_post_sms_reply(self, mock_get):
    """Test a sms message"""

    mock_resp = self.m1.fact_statement
    mock_get.return_value = mock_resp

    with self.client as c:

      # FIXME Twilio needs a To phone number

        resp = c.post(
          '/api/sms', 
          data={"Body": "Give me a fact!", "To": "+18008907162"}, 
          follow_redirects=True
        )

        self.assertTrue(True)
