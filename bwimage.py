import replicate
import os
from utilities import DBUpdateARG, DBReadARG, DBRead

def BWImageAPI(imgFile, model, renderFactor, userSession):
    result = {}
    try:
        output = replicate.run("arielreplicate/deoldify_image:0da600fab0c45a66211339f1c16b71345d22f26ef5fea3dca1bb90bb5711e950",input={"input_image": open(imgFile,'rb+'),'model_name':model,'render_factor':int(renderFactor)})
        images_count = int(DBReadARG('user','images_count','email',userSession,result))
        images_count += 1
        DBUpdateARG('user','images_count',images_count,'email',userSession)
        return output,'', images_count
    
    except Exception as error:
        images_count = int(DBReadARG('user','images_count','email',userSession,result))
        return '', error, images_count
