from flask import Flask, render_template
from flask_ask import Ask, statement, question
import requests
# from readability import Document
import os
from pygoogling.googling import GoogleSearch
import tldextract
# from newspaper import Article
# import lassie

# patching stable version of newspaper for compatibility with AWS LAmbda. Can be removed in future
# only /tmp is writable on lambda env
# os.environ['NEWSPAPER_BASE_DIRECTORY'] = '/tmp'
# os.environ['NLTK_DATA'] = '/tmp'
# Setting the env vars from zappa_settings

# https://stackoverflow.com/a/44532317/2523414
# no sqlite in lambda, needed by a small subset of nltk
import imp
import sys
sys.modules["sqlite"] = imp.new_module("sqlite")
sys.modules["sqlite3.dbapi2"] = imp.new_module("sqlite.dbapi2")

from newspaper import Article
# import nltk
# nltk.download('punkt')

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
        # webpage = requests.get(lucky_url)
        article = Article(lucky_url)
        article.download()
        article.parse()
        # resp = lassie.fetch(lucky_url)

        ext = tldextract.extract(lucky_url)
        domain = ext.registered_domain
        print("$"*50)
        print(search_query)
        # print(resp)
        print("$"*50)
        # content = resp["description"]
        # title = resp["title"]
        content = article.summary if article.summary else article.text
        title = article.title
        print("*"*50)
        print(lucky_url, domain, content)
        print("*" * 50)
    except IndexError:
        return question("Can you please repeat the query?")

    card_title = render_template('result_card_title').format(APP_NAME=APP_NAME, search_query=search_query)
    reply = render_template('result').format(APP_NAME=APP_NAME, content=content, domain=domain, title=title)
    text = render_template('result_card_text').format(APP_NAME=APP_NAME, domain=domain, shortened_content=content[:125]+"...")
    # prompt = render_template('launch_card_prompt').format(APP_NAME=APP_NAME)
    # return question(reply).reprompt(prompt).simple_card(card_title, text)
    return statement(reply).simple_card(card_title, text)

@ask.intent('AMAZON.HelpIntent')
def help():
    reply = render_template('help')
    # reprompt = render_template('help_prompt')
    text = render_template('help_card_text')
    title = render_template('help_card_title')
    return statement(reply).simple_card(title, text)