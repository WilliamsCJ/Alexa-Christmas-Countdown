from src/alexa_christmas_countdown import lambda_handler
import pytest

# Creating the json files
with open('when_is_christmas_input.json') as when_is_christmas_json:
    when_is_christmas = json.load(when_is_christmas_json)

with open('welcome_input.json') as welcome_json:
    welcome = json.load(welcome_json)

with open('how_long_to_christmas_input.json') as how_long_to_christmas_json:
    how_long_to_christmas = json.load(how_long_to_christmas_json)

# Test functions
def test_when_is_christmas(input):
    response = lambda_handler(input)
    assert response['body']['response']['card']['title'] == "When is Christmas?"

def test_welcome(input):
    response = lambda_handler(input)
    assert response['body']['response']['card']['title'] == "Welcome to Alexa's Christmas Countdown"

def test_how_long_to_christmas(input):
    response = lambda_handler(input)
    assert response['body']['response']['card']['title'] == "How long until Christmas?"
