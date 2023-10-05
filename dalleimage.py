import openai
from utitlities import DBUpdateARG, DBReadARG, DBRead


def DalleImageAPI(prompt, numberOfImage, size, userSession):
    try:
        result = {}
        image = openai.Image.create(
            prompt=prompt,
            n=int(numberOfImage),
            size=size
        )
        images_count = int(DBReadARG("user", "images_count", "email", userSession, result))
        updatedImage = images_count+int(numberOfImage)
        DBUpdateARG('user','images_count',updatedImage,'email',userSession)
        imagesurl = [item["url"] for item in image["data"]]
        return imagesurl, updatedImage
    except Exception as e:
        images_count = int(DBReadARG("user", "images_count", "email", userSession, result))
        return e , images_count




