from flask import request, current_app
import requests
import random

def get_random_fact():
  """
  Get a random fact from a random category.

  Output:
      fact_statement (str) 
  """

  if current_app.config["TESTING"] == True:
    url_root = "http://127.0.0.1:5000/"

  else:
    url_root = request.url_root

  fact_statement = None

  while not fact_statement:
    category = random.choice(['math', 'dates', 'trivia', 'years'])

    try:
      resp_ = requests.get(f"{url_root}api/{category}/random")
      resp_json = resp_.json()
      fact = resp_json.get("fact", {})
      fact_statement = fact.get("statement", None)
      break

    except:
      pass

  return fact_statement



