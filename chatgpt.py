import openai
from utilities import DBUpdateARG, DBReadARG, DBRead, count_words


def ChatGPTAPI(prompt, userSession):
    result = {}
    try:
        response = openai.ChatCompletion.create(
        # model="gpt-3.5-turbo-16k",
        model="gpt-4o",
        # "messages": [{"role": "user", "content": "Hello!"}],   --> Test message
        messages=[{"role": "user", "content": prompt}],
        temperature=1,
        # max_tokens=8000,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0
        )
        words_count = int(DBReadARG('user','words_count','email',userSession,result))
        words_to_update = count_words(response.choices[0].message.content) + words_count
        DBUpdateARG('user','words_count',words_to_update,'email',userSession)
        return response.choices[0].message.content, words_to_update
    except Exception as error:
        words_count = int(DBReadARG('user','words_count','email',userSession,result))
        return error, words_count
    
