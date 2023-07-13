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
def summarise_text(text, max_length=3000): # 完整的最大token是4097，但是回复还要用token
    tokens_estimate = len(text)   # estimated token count
    print(f'tokens_estimate: {tokens_estimate}')
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
        paragraphs = textwrap.wrap(text, max_length)
        print(f'text is longer than max_length, cutting it into {len(paragraphs)} paragraphs first and then preparing sumarizing with prompt:\n'
        f'{prompt_instructions}')

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
            summary += part_summary + "\n"

    return summary


# Handler for text messages
def reply_text(message):
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                     message)

    if url: # 目前只支持微信文章
        print('get an url and scrap the text first')
        res = requests.get(url[0])
        soup = BeautifulSoup(res.text, 'html.parser')

        # 找到并获取文章标题
        title_element = soup.find(class_='rich_media_title')
        if title_element:
            title = title_element.text.strip()
        else:
            title = 'No title found.'

        # 找到并获取文章内容
        content_element = soup.find(id='js_content')

        if content_element:
            content_spans = content_element.find_all('span')
            content = ' '.join(span.text for span in content_spans)
        else:
            content = 'No content found.'

        # 将标题和内容组合在一起
        text = title + '\n\n' + content + '\n\n' + url[0]
        summary = summarise_text(text)
        return summary
    else:
        return "我能帮你做什么."