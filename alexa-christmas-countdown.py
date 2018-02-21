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


def help_response():
    session_attributes = {}
    card_title = "What can I do?"
    speech_output = "You can ask me: "\
                    "How many days is it until Christmas, or when is Christmas?"
    reprompt_text = "Please ask me how many days it is until Christmas"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


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
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return do_welcome()


def on_intent(intent_request, session):
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to control functions
    if intent_name == "WhenIsChristmas":
        return when_is_christmas()
    elif intent_name == "HowLongUntilChristmas":
        return how_long_until_christmas()
    elif intent_name == "AMAZON.HelpIntent":
        return help_response()
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


# Main handler to deal with incoming JSON requests and trigger the right event


def lambda_handler(event, context):

    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

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
