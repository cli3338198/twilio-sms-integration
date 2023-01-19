from nums_api.database import db
from nums_api.maths.models import Math

# seed data for sms

m1 = Math(
  number=1,
  fact_fragment='fact fragment for m1.',
  fact_statement='1 is the loneliest number.',
  was_submitted=False
)

m2 = Math(
  number=2,
  fact_fragment='fact fragment for m2.',
  fact_statement='2 is the double of 1.',
  was_submitted=False
)

db.session.add(m1)
db.session.add(m2)
db.session.commit()