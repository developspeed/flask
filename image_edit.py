import replicate
import os
from utitlities import DBUpdateARG, DBReadARG, DBRead


def ImageEditAPI(imageFile, userprompt, neg_prompt, user_output_images, userSession):
    result = {}
    try:
        output = replicate.run(
            "timothybrooks/instruct-pix2pix:30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f",
            input={
                "image": open(imageFile,'rb'),
                "prompt": userprompt,
                "negative_prompt": neg_prompt,
                "num_outputs": user_output_images,
            },
        )
        images_count = int(DBReadARG("user", "images_count", "email", userSession,result))
        updated_images = 0
        if int(user_output_images) == 1:
            updated_images = images_count + 1
        else:
            updated_images = images_count + 4
        DBUpdateARG('user','images_count',updated_images,'email',userSession)
        return output,'', updated_images
    except Exception as error:
        images_count = int(DBReadARG("user", "images_count", "email", userSession,result))
        return '', error, images_count
