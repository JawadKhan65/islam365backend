from app import gemini, genai
import os
import csv
import anthropic
from prompts import *
from dotenv import load_dotenv
import google.generativeai as genai
import textwrap
from IPython.display import Markdown


# athropic_api = load_dotenv
# client = anthropic.Anthropic()
# sonnet = "claude-3-5-sonnet-20240620"

gemini = 'AIzaSyCnhGHna9kU6-fmolRVc7WdEgehyCOYTSU'
os.environ['GOOGLE_API_KEY'] = gemini
genai.configure(api_key=gemini)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")


def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


def gemini_model(query):
    response = model.generate_content(
        [SEARCH_SYSTEM, query])
    print("Search Query Insigths: ")
    questions = response.text.split(',')
    return questions


def content_generator(query):
    response = model.generate_content(
        [CONTENT_GENERATOR, query])
    response = response.text
    return response


def penalize(initial_data):
    response = model.generate_content(
        [PENALIZER_SYSTEM, initial_data])
    # print(response.text)
    response = response.text
    return response


def generate(penalized):
    response = model.generate_content(
        [GENERATOR_SYSTEM+"Note:ADD references from quran and hadiths if relates to that topic and Dont add the line that while i dont have access or something like this you just have to give necessary information not concerned with what you can or not ok just give precise and authentic information about the content if you consider ahadith should be added for reference  or some reference to be added you should add it and length should be same as provided text.You will just enhance the quality of content maintaining orignal lengt.AGAIN NOTE THAT REFERENCES ARE MUST AND SHOULD BE AUTHENTIC.", penalized])
    response = response.text

    # print(response.text)
    return response


def RAG_ANALYZER(rag_content):
    response = model.generate_content([RAG_ANALYZER_SYSTEM, rag_content])
    response = response.text
    print(response)

    return response


def RAG_SYSTEM(similar_docs):
    response = model.generate_content([RAG_SYSTEM_PROMPT, str(similar_docs)])
    response = response.text
    return response
