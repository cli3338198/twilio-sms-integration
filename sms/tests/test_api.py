from unittest import TestCase, mock
from nums_api import app
from nums_api.database import db, connect_db
from nums_api.config import DATABASE_URL_TEST
from nums_api.maths.models import Math
from nums_api.sms.api import get_random_fact


app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

connect_db(app)

db.drop_all()
db.create_all()

class SMSBaseAPITestCase(TestCase):
  """
      Test for SMS API.
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

      self.m2 = Math(
          number=1,
          fact_fragment="the number for this m2 test fact fragment",
          fact_statement="2 is the double of 1.",
          was_submitted=False,
      )

      db.session.add(self.m1)
      db.session.commit()

      self.client = app.test_client()

  def tearDown(self):
      """Clean up any fouled transaction."""

      db.session.rollback()


class SMSAPITestCase(SMSBaseAPITestCase):

  def test_setup(self):
      """Test to make sure tests are set up correctly"""

      test_setup_correct = True
      self.assertEqual(test_setup_correct, True)

  def _mock_response(
            self,
            status=200,
            json={
            "fact": {
                "fragment": "the number for this m1 test fact fragment",
                "statement": "1 is the number for this m1 test fact statement.",
                "number": 1,
                "type": "math"
            }
        }): 
      """Mock response for requests.get"""

      mock_resp = mock.Mock()
      mock_resp.status_code = status
      mock_resp.json = mock.Mock(
        return_value=json
      )
      
      return mock_resp

  @mock.patch('requests.get')
  def test_get_random_fact(self, mock_get):
    """Test get a random fact"""
    
    mock_resp = self._mock_response()
    mock_get.return_value = mock_resp

    random_fact = get_random_fact()
    self.assertEqual(random_fact, self.m1.fact_statement)

  @mock.patch('requests.get')
  def test_get_random_fact_v2(self, mock_get):
    """Test the mock is behaving correctly"""

    mock_resp = self._mock_response(json={
            "fact": {
                "fragment": "the number for this m2 test fact fragment",
                "statement": "2 is the double of 1.",
                "number": 2,
                "type": "math"
            }
        })
    mock_get.return_value = mock_resp

    random_fact = get_random_fact()
    self.assertEqual(random_fact, self.m2.fact_statement)
    
  # def test_get_random_fact_v2(self):
  #   """Test get a random fact v2"""

  #   with mock.patch("nums_api.sms.api.requests.get") as mock_request:
  #     mock_request.return_value = self._mock_response()

  #     mock_request.url_root = "http://127.0.0.1:5000/"
  #     breakpoint()
  #     self.assertEqual(get_random_fact(), self._mock_response)
