from __future__ import print_function
import datetime


# Response Building Helpers. Courtesy of Amazon.

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

# Control Functions

def do_welcome():
    session_attributes = {}
    card_title = "Welcome to Alexa's Christmas Countdown"
    speech_output = "Welcome to my Christmas Countdown. " \
                    "All you need to do is ask me: "\
                    "How many days is it until Christmas, or when is Christmas?"
    reprompt_text = "Please ask me how many days it is until Christmas"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def when_is_christmas():
    session_attributes = {}
    card_title = "Christmas is on December 25th"
    speech_output = "Christmas is on December 25th."
    reprompt_text = "Sorry I didn't get that."\
                    "Try again!"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def how_long_until_christmas():
    session_attributes = {}
    card_title = "There are " + get_date() + " days until Christmas."
    speech_output =  "There are " + get_date() + " days until Christmas. "\
                     "I'm so excited!"
    reprompt_text = "Sorry I didn't get that."\
                   "Ask again!"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_date():
    current = datetime.date.today()
    christmas = datetime.date(datetime.date.today().year, 12, 25)
    days_until = christmas - current
    return (str(days_until.days)[0:])


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using Alexa's Christmas Countdown." \
                    "Have a great day!"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


# Events


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return do_welcome()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "WhenIsChristmas":
        return when_is_christmas()
    elif intent_name == "HowLongUntilChristmas":
        return how_long_until_christmas()
    elif intent_name == "AMAZON.HelpIntent":
        return do_welcome
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# Main handler

def lambda_handler(event):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    if (event['session']['application']['applicationId'] !=
            "amzn1.ask.skill.39162ea8-418d-4808-aaf5-85bc824f3207"):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
        print ("Done")
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


event = {
	"version": "1.0",
	"session": {
		"new": False,
		"sessionId": "amzn1.echo-api.session.c9851bda-bcb8-4ed8-985f-3014795139fc",
		"application": {
			"applicationId": "amzn1.ask.skill.39162ea8-418d-4808-aaf5-85bc824f3207"
		},
		"user": {
			"userId": "amzn1.ask.account.AGMMJ4VTBWHZZYY7GZYMTQ36JXZF7S7Q2HH4NF3ZD6TBUKB67Z3VMJQERFIOC33NCIZW7Y6GIC2TRPSKVXWLJP3RDM6DPDOP7YE72SSBQLBZ3NGFVYVR5NP3WKLREQ27KZQVU53FAMMNBSYZSDJEIOCYXZPIJG64ODFDMRPSD577MYYDBVDTCEY5ZRB6LJQNDIED6GTTSGSDN5A"
		}
	},
	"context": {
		"AudioPlayer": {
			"playerActivity": "IDLE"
		},
		"Display": {
			"token": ""
		},
		"System": {
			"application": {
				"applicationId": "amzn1.ask.skill.39162ea8-418d-4808-aaf5-85bc824f3207"
			},
			"user": {
				"userId": "amzn1.ask.account.AGMMJ4VTBWHZZYY7GZYMTQ36JXZF7S7Q2HH4NF3ZD6TBUKB67Z3VMJQERFIOC33NCIZW7Y6GIC2TRPSKVXWLJP3RDM6DPDOP7YE72SSBQLBZ3NGFVYVR5NP3WKLREQ27KZQVU53FAMMNBSYZSDJEIOCYXZPIJG64ODFDMRPSD577MYYDBVDTCEY5ZRB6LJQNDIED6GTTSGSDN5A"
			},
			"device": {
				"deviceId": "amzn1.ask.device.AEJ727BEORRA6Z3FYYPJ3TUJX664KWBQBAALSHAW7SKXSMDKODNW5Z2VNMF6JUNWZTNG4NZU4VJTSGHHK6MU75J66PNGLAMTRKCNGC6CSVBMHO33GAXVVHHIK7GLQBFOLFAJF66FFUVMSC4UDSRYC4OUODBQ",
				"supportedInterfaces": {
					"AudioPlayer": {},
					"Display": {
						"templateVersion": "1.0",
						"markupVersion": "1.0"
					}
				}
			},
			"apiEndpoint": "https://api.eu.amazonalexa.com",
			"apiAccessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjEifQ.eyJhdWQiOiJodHRwczovL2FwaS5hbWF6b25hbGV4YS5jb20iLCJpc3MiOiJBbGV4YVNraWxsS2l0Iiwic3ViIjoiYW16bjEuYXNrLnNraWxsLjM5MTYyZWE4LTQxOGQtNDgwOC1hYWY1LTg1YmM4MjRmMzIwNyIsImV4cCI6MTUxOTE1MTU5MCwiaWF0IjoxNTE5MTQ3OTkwLCJuYmYiOjE1MTkxNDc5OTAsInByaXZhdGVDbGFpbXMiOnsiY29uc2VudFRva2VuIjpudWxsLCJkZXZpY2VJZCI6ImFtem4xLmFzay5kZXZpY2UuQUVKNzI3QkVPUlJBNlozRllZUEozVFVKWDY2NEtXQlFCQUFMU0hBVzdTS1hTTURLT0ROVzVaMlZOTUY2SlVOV1pUTkc0TlpVNFZKVFNHSEhLNk1VNzVKNjZQTkdMQU1UUktDTkdDNkNTVkJNSE8zM0dBWFZWSEhJSzdHTFFCRk9MRkFKRjY2RkZVVk1TQzRVRFNSWUM0T1VPREJRIiwidXNlcklkIjoiYW16bjEuYXNrLmFjY291bnQuQUdNTUo0VlRCV0haWllZN0daWU1UUTM2SlhaRjdTN1EySEg0TkYzWkQ2VEJVS0I2N1ozVk1KUUVSRklPQzMzTkNJWlc3WTZHSUMyVFJQU0tWWFdMSlAzUkRNNkRQRE9QN1lFNzJTU0JRTEJaM05HRlZZVlI1TlAzV0tMUkVRMjdLWlFWVTUzRkFNTU5CU1laU0RKRUlPQ1lYWlBJSkc2NE9ERkRNUlBTRDU3N01ZWURCVkRUQ0VZNVpSQjZMSlFORElFRDZHVFRTR1NETjVBIn19.a_Q204Z9p3wCn5nf8BlAmNtSgA1zNwo7ukrR1JcD1jBj6NgPLZPw3rVYxIfOBCJbr6XlaC_fNjoCKS9UDw-SWiMn-LBgdvcDOkN_iT2oDCVuluAqb0ebeM2dzW4qAn42zFQz-RXzhkC93IQ-fqnkws1n6OM9WlSFrhNhjxkYfkVFCdghx3RSe9cpjtOx7QmZngXPLVI5zT2l8fDX6597ztr6k7GBD20NdLbv47sEFm5-SnGZ1HXBdY9JnFX57MBa7ZIOluFDKWQJBiFHGjJzsJjyPXxrMPkCOix751mzFQMeNyyehpARLPRJUzUtGGoizNmXgJm5OLYj3HaXieFYyQ"
		}
	},
	"request": {
		"type": "IntentRequest",
		"requestId": "amzn1.echo-api.request.3513c005-b7f2-498a-aea1-95382e22e51e",
		"timestamp": "2018-02-20T17:33:10Z",
		"locale": "en-GB",
		"intent": {
			"name": "HowLongUntilChristmas",
			"confirmationStatus": "NONE"
		}
	}
}

lambda_handler(event)
