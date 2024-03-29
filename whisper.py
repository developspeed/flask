# This is the function for whisper components
import openai
import replicate
import os
from utilities import DBUpdateARG, DBReadARG, DBRead, custom_round

def WhisperMICAPI(audioFile, duration, userSession, task):
    output = replicate.run("openai/whisper:91ee9c0c3df30478510ff8c8a3a545add1ad0259ad3a9f78fba57fbc05ee64f7",
                                           input={"audio": open(audioFile,'rb'),"translate":True,"model":'large-v2'})
                                           
    result = {}
    minutes_count = custom_round(float(DBReadARG('user','minutes_count','email',userSession,result)))
    minutes_to_update = custom_round(float(minutes_count+duration))
    DBUpdateARG('user','minutes_count',minutes_to_update,'email',userSession)
    if task == 'transcribe':
        return output['transcription'], output['detected_language'], minutes_to_update
    else:
        return output['translation'], output['detected_language'], minutes_to_update

               
def WhisperFileAPI(audioFile, duration, userSession, task):
    if task == 'transcribe':
        output =  openai.Audio.transcribe("whisper-1", open(audioFile,'rb'))
        text = output['text'][:1000]
        # Detecting the Language of the Text
        prompt = (f"Please determine the language of the following text:\n\n{text}\n\n"
                    "The language is:")
        completions = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1,
            n=1,
            stop=None,
            temperature=0.5,
        )
        result = {}
        language = completions.choices[0].text.strip()
        minutes_count = custom_round(float(DBReadARG('user','minutes_count','email',userSession,result)))
        minutes_to_update = custom_round(float(minutes_count+duration))
        DBUpdateARG('user','minutes_count',minutes_to_update,'email',userSession)
        return output['text'], language, minutes_to_update
    else:
        output =  openai.Audio.translate("whisper-1", open(audioFile,'rb'))
        result = {}
        minutes_count = custom_round(float(DBReadARG('user','minutes_count','email',userSession,result)))
        minutes_to_update = custom_round(float(minutes_count+duration))
        DBUpdateARG('user','minutes_count',minutes_to_update,'email',userSession)
        return output['text'], "" , minutes_to_update
