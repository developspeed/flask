import openai
import os
from utitlities import DBUpdateARG, DBReadARG, DBRead

# Initializing Tokkens
openai.api_key = DBRead('whisper_config','API_KEY')

def ChatGPTAPI(prompt, words_to_update, userSession):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0,
    max_tokens=60,
    top_p=1,
    frequency_penalty=0.5,
    presence_penalty=0
    )

    words_count = int(DBReadARG('user','words_count','email',userSession))
    words_to_update = words_to_update + words_count
    DBUpdateARG('user','words_count',words_to_update,'email',userSession)
    return response.choices[0].text.strip(), words_to_update


    