# coding:utf-8
import os
import re
import requests
from bs4 import BeautifulSoup
import openai
from dotenv import load_dotenv
import textwrap

# Load OpenAI key
load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

with open('prompt.txt', 'r') as f:
    prompt_instructions = f.read()

# Function to summarize text
def summarise_text(text, max_length=2048):
    tokens_estimate = len(text) / 6  # estimated token count

    if tokens_estimate <= max_length:
        print(f'text is less than max_length, preparing summarizing with prompt:{prompt_instructions}')
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"{text}\n{prompt_instructions}"}
            ],
        )
        summary = chat.choices[0].message['content'].strip()

    else:
        print(
            f'text is longer than max_length, cutting it into paragraphs first and then preparing sumarizing with prompt:{prompt_instructions}')
        paragraphs = textwrap.wrap(text, max_length)

        summary = ""
        for para in paragraphs:
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"{para}\n{prompt_instructions}"}
                ],
            )

            part_summary = chat.choices[0].message['content'].strip()
            summary += part_summary

    return summary


# Handler for text messages
def reply_text(message):
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                     message)
    if url:
        print('get an url and scrap the text first')
        res = requests.get(url[0])
        soup = BeautifulSoup(res.text, 'html.parser')
        text = ''.join(p.text for p in soup.find_all('p'))
        summary = summarise_text(text)
        return summary
    else:
        return "我能帮你做什么."