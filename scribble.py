import replicate
import os
from utitlities import DBUpdateARG, DBReadARG, DBRead, custom_round

# Initializing Tokens
os.environ['REPLICATE_API_TOKEN'] = str(DBRead('scribble','API_KEY'))

def ScribbleAPI(image,prompt,userSession):
    result = {}
    try:
        output = replicate.run(
            "nevernotsean/scribble-stories:c1f1f32ea543c5b6a8f3968f167ce02aff1e27cd25c1234f49c5bc15e556b19d",
            input={"image": open(image,'rb'),'prompt':prompt}
        )
        images_count = int(DBReadARG('user','images_count','email',userSession,result))
        images_count += 1
        DBUpdateARG('user','images_count',images_count,'email',userSession)
        return output,'', images_count
    except Exception as error:
        images_count = int(DBReadARG('user','images_count','email',userSession,result))
        return '',error, images_count
    