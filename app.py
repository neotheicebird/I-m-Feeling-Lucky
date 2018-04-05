from flask import Flask, render_template
from flask_ask import Ask, statement, question
import requests
from readability import Document
import os
from pygoogling.googling import GoogleSearch
import tldextract

app = Flask(__name__)
ask = Ask(app, '/')

app.secret_key = os.urandom(24)

APP_NAME = "I'm Feeling Lucky"

@ask.launch
def launch():
    """
    If user says e.g "Alexa, open I m feeling lucky"
    :return:
    """
    card_title = render_template('launch_card_title').format(APP_NAME=APP_NAME)
    reply = render_template('launch').format(APP_NAME=APP_NAME)
    text = render_template('launch_card_text').format(APP_NAME=APP_NAME)
    prompt = render_template('launch_card_prompt').format(APP_NAME=APP_NAME)
    return question(reply).reprompt(prompt).simple_card(card_title, text)

@ask.intent('feeling_lucky')
def feeling_lucky(search_query):
    """
    Search
    :return:
    """
    try:
        search_request = GoogleSearch(search_query)
        search_request.start_search(max_page=1)
        lucky_url = search_request.search_result.pop(0)
        webpage = requests.get(lucky_url)
        doc = Document(webpage.text)
        ext = tldextract.extract(lucky_url)
        domain = ext.registered_domain
        content = doc.content()
    except IndexError:
        return

    card_title = render_template('result_card_title').format(APP_NAME=APP_NAME, search_query=search_query)
    reply = render_template('result').format(APP_NAME=APP_NAME, content=content, domain=domain)
    text = render_template('result_card_text').format(APP_NAME=APP_NAME, domain=domain, shortened_content=content[:125]+"...")
    # prompt = render_template('launch_card_prompt').format(APP_NAME=APP_NAME)
    # return question(reply).reprompt(prompt).simple_card(card_title, text)
    return statement(reply).simple_card(card_title, text)

@ask.intent('AMAZON.HelpIntent')
def help():
    reply = render_template('help')
    reprompt = render_template('help_prompt')
    text = render_template('help_card_text')
    title = render_template('help_card_title')
    return question(reply).reprompt(reprompt).simple_card(title, text)