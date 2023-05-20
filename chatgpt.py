import openai
import os
from utitlities import DBUpdateARG, DBReadARG, DBRead, count_words

# Initializing Tokkens
openai.api_key = DBRead('whisper_config','API_KEY')

def ChatGPTAPI(prompt, userSession):
    result = {}
    try:
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1,
        max_tokens=4000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
        words_count = int(DBReadARG('user','words_count','email',userSession,result))
        words_to_update = count_words(response.choices[0].text.strip()) + words_count
        DBUpdateARG('user','words_count',words_to_update,'email',userSession)
        return response.choices[0].text.strip(), words_to_update
    except Exception as error:
        words_count = int(DBReadARG('user','words_count','email',userSession,result))
        return error, words_count
