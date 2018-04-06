# https://stackoverflow.com/a/44532317/2523414
# no sqlite in lambda, needed by a small subset of nltk
import imp
# from readability import Document
import os
import sys

import tldextract
from flask import Flask, render_template
from flask_ask import Ask, question
from pygoogling.googling import GoogleSearch
from summarizer.summarize import summarize

# from newspaper import Article
# patching stable version of newspaper for compatibility with AWS LAmbda. Can be removed in future
# only /tmp is writable on lambda env
# os.environ['NEWSPAPER_BASE_DIRECTORY'] = '/tmp'
# os.environ['NLTK_DATA'] = '/tmp'
# Setting the env vars from zappa_settings
sys.modules["sqlite"] = imp.new_module("sqlite")
sys.modules["sqlite3.dbapi2"] = imp.new_module("sqlite.dbapi2")

import newspaper
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
    card_title = render_template('launch_card_title')
    reply = render_template('launch')
    text = render_template('launch_card_text')
    prompt = render_template('launch_card_prompt')
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
        for x in range(5):    # Try upto 5 links from top. If all raises error, quit
            try:
                lucky_url = search_request.search_result.pop(0)
                # webpage = requests.get(lucky_url)
                article = Article(lucky_url)
                article.download()
                article.parse()
                break
            except newspaper.article.ArticleException:
                print("Error encountered, Article parsing. URL: ", lucky_url)
                continue
        else:
            # will run if break doesnt execute
            return question("Sorry, I am unable to get proper results for this query. Please try something else")

        # resp = lassie.fetch(lucky_url)

        ext = tldextract.extract(lucky_url)
        domain = ext.registered_domain
        print("$"*50)
        print(search_query)
        # print(resp)
        print("$"*50)
        # content = resp["description"]
        # title = resp["title"]
        title = article.title
        content = article.summary if article.summary else summarize(article.text, 2000)    # max words for a skill result is 8000
        print("*"*50)
        print(lucky_url, domain, content)
        print(title)
        print("*" * 50)
    except IndexError:
        return question("Can you please repeat the query?")

    card_title = render_template('result_card_title').format(search_query=search_query)
    reply = render_template('result').format(content=content, domain=domain, title=title)
    text = render_template('result_card_text').format(domain=domain, shortened_content=content[:125]+"...")
    prompt = render_template('launch_card_prompt')
    # return question(reply).reprompt(prompt).simple_card(card_title, text)
    return question(reply).reprompt(prompt).simple_card(card_title, text)

@ask.intent('AMAZON.HelpIntent')
def help():
    reply = render_template('help')
    # reprompt = render_template('help_prompt')
    text = render_template('help_card_text')
    title = render_template('help_card_title')
    prompt = render_template('launch_card_prompt')
    return question(reply).reprompt(prompt).simple_card(title, text)