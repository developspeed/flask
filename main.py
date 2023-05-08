from decimal import Decimal
from flask import Flask, render_template, request, redirect, session, url_for, jsonify
import mysql.connector as ms
import os
import replicate
from io import BytesIO
import openai


cnx = ms.connect(user='magic_register', password='Indira@2000',
                 host='185.104.29.84', database='magic_register')
cursor = cnx.cursor()


# Setting the Environment of the application using the API token of Replicate from the database
get_API_key_query = "SELECT `API_KEY` FROM `image_edit_config`"
cursor.execute(get_API_key_query)
get_API_key = cursor.fetchone()[0]
os.environ['REPLICATE_API_TOKEN'] = str(get_API_key)

get_API_key_query = "SELECT `API_KEY` FROM `whisper_config`"
cursor.execute(get_API_key_query)
get_API_key = cursor.fetchone()[0]
openai.api_key = str(get_API_key)



# Closing the DB Connection
cursor.close()
cnx.close()

app = Flask(__name__, static_url_path='/static')
app.secret_key = '5gfdfdsdr345dgfs45dgfdgdfg09043532%##$h2h340adsf9'



@app.route("/")
# @app.route("/login")
def login():
    return render_template('login.html')


@app.route("/", methods=['POST', 'GET'])
def Authenticate():
    # connecting to database...
    cnx = ms.connect(user='magic_register', password='Indira@2000',
                     host='185.104.29.84', database='magic_register')
    cursor = cnx.cursor()

    email = request.form['email']
    login_code = request.form['login_code']

    # You can add code here to validate the user's login information
    check_for_cred = f"SELECT `phytonlogin` FROM `user` WHERE `email` = '{email}'"
    cursor.execute(check_for_cred)
    session['get_user_email'] = email

    auth_code = cursor.fetchone()[0]

    cursor.close()
    cnx.close()
    if login_code != auth_code:
        return render_template("login.html", data="Incorrect Email or Password")
    else:
        return redirect(url_for('Dashboard'))


@app.route('/logout')
def logout():
    session.pop('get_user_email', None)  # remove the email from the session
    return redirect(url_for('login'))


admin_name_validation = ""


@app.route("/dashboard")
def Dashboard():
    if 'get_user_email' in session:
        cnx = ms.connect(user='magic_register', password='Indira@2000',
                         host='185.104.29.84', database='magic_register')
        cursor = cnx.cursor()
        email = session.get("get_user_email")

        ########## Getting the User data using Email from database ###########
        name_query = f"SELECT `name` FROM `user` WHERE `email` = '{email}'"
        cursor.execute(name_query)
        name = cursor.fetchone()[0]
        global admin_name_validation
        admin_name_validation = name

        # Subscription Details
        subscription_end_query = f"SELECT `end_subscription_period` FROM `user` WHERE `email` = '{email}'"
        cursor.execute(subscription_end_query)
        subscription_end = cursor.fetchone()[0]

        # Words Usage
        words_total_query = f"SELECT `words_total` FROM `user` WHERE `email` = '{email}'"
        cursor.execute(words_total_query)
        words_total = cursor.fetchone()[0]

        words_count_query = f"SELECT `words_count` FROM `user` WHERE `email` = '{email}'"
        cursor.execute(words_count_query)
        words_count = cursor.fetchone()[0]

        # Image Usage
        images_total_query = f"SELECT `images_total` FROM `user` WHERE `email` = '{email}'"
        cursor.execute(images_total_query)
        images_total = cursor.fetchone()[0]

        images_count_query = f"SELECT `images_count` FROM `user` WHERE `email` = '{email}'"
        cursor.execute(images_count_query)
        images_count = cursor.fetchone()[0]

        # Minutes Usage
        minutes_total_query = f"SELECT `minutes_total` FROM `user` WHERE `email` = '{email}'"
        cursor.execute(minutes_total_query)
        minutes_total = cursor.fetchone()[0]

        minutes_count_query = f"SELECT `minutes_count` FROM `user` WHERE `email` = '{email}'"
        cursor.execute(minutes_count_query)
        minutes_count = cursor.fetchone()[0]
        minutes_to_show = custom_round(minutes_count)

        cursor.close()
        cnx.close()
        return render_template("dashboard.html", data={'name': name, 'subscription_end': subscription_end, 'words_total': words_total, 'words_count': words_count, 'images_total': images_total, 'images_count': images_count, 'minutes_total': minutes_total, 'minutes_count': minutes_to_show})

    else:
        return redirect(url_for("login"))


############################### Whisper AI Functions ######################################


def custom_round(num, digits=2, Isstr=False):
    tmp = Decimal(num)
    x = ("{0:.%sf}" % digits).format(round(tmp, digits))
    if Isstr:
        return x
    return float(Decimal(x))


# Audio Upload through Mic and files with duration and other options
audioRecordedGlobal = None
minutes_to_update = 0


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    global audioRecordedGlobal
    audioRecordedGlobal = request.files.get('audio')
    # Save the audio file to the current directory
    file_path = os.path.join(os.getcwd(), 'audio.mp3')
    audioRecordedGlobal.save(file_path)
    print(audioRecordedGlobal.filename)
    global minutes_to_update
    minutes_to_update = request.form.get('duration')
    return "Done"



@app.route('/whisper', methods=['POST', 'GET'])
def Whisper():
    if 'get_user_email' in session:

        cnx = ms.connect(user='magic_register', password='Indira@2000',
                         host='185.104.29.84', database='magic_register')
        cursor = cnx.cursor()

        email = session['get_user_email']
        minutes_count_query = f"SELECT `minutes_count` FROM `user` WHERE `email` = '{email}'"
        cursor.execute(minutes_count_query)
        minutes_count = cursor.fetchone()[0]
        minutes_to_show = custom_round(minutes_count)

        minutes_total_query = f"SELECT `minutes_total` FROM `user` WHERE `email` = '{email}'"
        cursor.execute(minutes_total_query)
        minutes_total = cursor.fetchone()[0]

        WhisperAIText = DBRead('whisper_config', 'whisper_text')

        cursor.close()
        cnx.close()
        return render_template('whisper.html', data=[minutes_to_show, minutes_total, WhisperAIText])

    else:
        return redirect(url_for("login"))


@app.route('/whisper-results', methods=["POST"])
def WhisperAI():
    cnx = ms.connect(user='magic_register', password='Indira@2000',
                     host='185.104.29.84', database='magic_register')
    cursor = cnx.cursor()
    email = session['get_user_email']

    minutes_count_query = f"SELECT `minutes_count` FROM `user` WHERE `email` = '{email}'"
    cursor.execute(minutes_count_query)
    minutes_count = float(cursor.fetchone()[0])

    minutes_total_query = f"SELECT `minutes_total` FROM `user` WHERE `email` = '{email}'"
    cursor.execute(minutes_total_query)
    minutes_total = cursor.fetchone()[0]

    cursor.close()
    cnx.close()
    # Reading the audio file and Converting the audio 
    audioFile = open("audio.mp3",'rb')
    
    global minutes_to_update
    minutes_to_update = custom_round(minutes_to_update)
    print("Uploaded Audio or File Size : ", minutes_to_update)
    
    task = request.form.get('task')
    print(task)

    if minutes_count <= float(minutes_total):
        # Model Running
        # Transcribing the audio    
        if task == "transcribe":
            try:
                
                output =  openai.Audio.transcribe("whisper-1", audioFile)
                text = output['text'][:2000]
                
                # Detecting the Language of the Text
                model_engine = "text-davinci-002"
                prompt = (f"Please determine the language of the following text:\n\n{text}\n\n"
                            "The language is:")
                completions = openai.Completion.create(
                    engine=model_engine,
                    prompt=prompt,
                    max_tokens=1,
                    n=1,
                    stop=None,
                    temperature=0.5,
                )
                language = completions.choices[0].text.strip()
                cnx = ms.connect(user='magic_register', password='Indira@2000',
                            host='185.104.29.84', database='magic_register')
                cursor = cnx.cursor()
                update_minutes_query = f"UPDATE `user` SET `minutes_count` = '{minutes_to_update+minutes_count}' WHERE `email` = '{email}';"
                cursor.execute(update_minutes_query)
                cnx.commit()
                cursor.close()
                cnx.close()

                print("The total minutes will be : ",minutes_count+minutes_to_update)
                
                minutes_to_show = custom_round(minutes_count+minutes_to_update)
                audioFile.close()
                os.remove("audio.mp3")

                return jsonify({'outputData': output['text'], 'language_detect': language, 'minutes_count': minutes_to_show, "minutes_total": minutes_total})
            except Exception as e:
                print(e)
                return jsonify({"outputData": e, 'translate': "", 'language_detect': '', 'minutes_count': minutes_count, "minutes_total": minutes_total})
            
        else:
            try:
                # We are again establishing a connection because large file give connection lost error
                output_translate =  openai.Audio.translate("whisper-1", audioFile)
                cnx = ms.connect(user='magic_register', password='Indira@2000',
                            host='185.104.29.84', database='magic_register')
                cursor = cnx.cursor()
                update_minutes_query = f"UPDATE `user` SET `minutes_count` = '{minutes_to_update+minutes_count}' WHERE `email` = '{email}';"
                cursor.execute(update_minutes_query)
                cnx.commit()
                cursor.close()
                cnx.close()

                print("The total minutes will be : ",minutes_count+minutes_to_update)

                minutes_to_show = custom_round(minutes_count+minutes_to_update)
                audioFile.close()
                os.remove("audio.mp3")

                return jsonify({'translate': output_translate['text'], 'minutes_count': minutes_to_show, "minutes_total": minutes_total})

            except Exception as e:
                print(e)
                return jsonify({"outputData": e, 'translate': "", 'language_detect': '', 'minutes_count': minutes_count, "minutes_total": minutes_total})
    else:
        return render_template('whisper.html', data=["", "", "", "", "", "You Have Used All Your Minutes"])


# Image Edit Model and Functions

@app.route("/image-edit")
def ImageEdit():
    if 'get_user_email' in session:

        cnx = ms.connect(user='magic_register', password='Indira@2000',
                         host='185.104.29.84', database='magic_register')
        cursor = cnx.cursor()

        email = session['get_user_email']
        images_count_query = f"SELECT `images_count` FROM `user` WHERE `email` = '{email}'"
        cursor.execute(images_count_query)
        images_count = cursor.fetchone()[0]

        images_total_query = f"SELECT `images_total` FROM `user` WHERE `email` = '{email}'"
        cursor.execute(images_total_query)
        images_total = cursor.fetchone()[0]

        ImageEditText = DBRead('image_edit_config', 'image_edit_text')

        cursor.close()
        cnx.close()
        return render_template('imagedit.html', data=[images_count, images_total, ImageEditText])

    else:
        return redirect(url_for("login"))

FilePath = None
@app.route('/upload-image',methods=["GET","POST"])
def upload_image():
    global FilePath
    FilePath = BytesIO(request.files.get('imageFile').read())
    print("The File",FilePath)
    return "Uploaded Successfully"

@app.route('/image-edit-results', methods=["POST"])
def ImageEditResults():
    cnx = ms.connect(user='magic_register', password='Indira@2000',
                     host='185.104.29.84', database='magic_register')
    cursor = cnx.cursor()
    email = session['get_user_email']

    images_count_query = f"SELECT `images_count` FROM `user` WHERE `email` = '{email}'"
    cursor.execute(images_count_query)
    images_count = int(cursor.fetchone()[0])

    images_total_query = f"SELECT `images_total` FROM `user` WHERE `email` = '{email}'"
    cursor.execute(images_total_query)
    images_total = int(cursor.fetchone()[0])
    
    userprompt = request.form.get('prompt')
    user_neg_prompt = request.form.get('neg_prompt')
    user_output_images = request.form.get('output_images')
    print(userprompt,user_neg_prompt,user_output_images)
    print("Working")
    if images_count < images_total:
        try:
            output = replicate.run(
                    "timothybrooks/instruct-pix2pix:30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f",
                    input={"image": FilePath,
                            'prompt':userprompt,
                            'negative_prompt':user_neg_prompt,
                            'num_outputs':int(user_output_images)
                            }
                )
            # print(output)
            print("Done")
            updated_images = 0
            if int(user_output_images) == 1:
                updated_images = images_count+1
            else:
                updated_images = images_count+4
            images_update_query = f"UPDATE `user` SET `images_count` = '{updated_images}' WHERE `email` = '{email}';"
            cursor.execute(images_update_query)
            cnx.commit()
            cursor.close()
            cnx.close()
            return render_template('imagedit-results.html',data=[updated_images,images_total,output,"",""])
        except Exception as e:
            print(e)
            return render_template('imagedit-results.html',data=[images_count,images_total,"","There's some problems in your image",""])
    else:
        return render_template('imagedit-results.html',data=[images_count,images_total,"","","You have used all your images"])
    

@app.route('/bw-image',methods=['GET',"POST"])
def BWImage():
    if 'get_user_email' in session:
        cnx = ms.connect(user='magic_register', password='Indira@2000',
                         host='185.104.29.84', database='magic_register')
        cursor = cnx.cursor()

        email = session['get_user_email']
        images_count_query = f"SELECT `images_count` FROM `user` WHERE `email` = '{email}'"
        cursor.execute(images_count_query)
        images_count = cursor.fetchone()[0]

        images_total_query = f"SELECT `images_total` FROM `user` WHERE `email` = '{email}'"
        cursor.execute(images_total_query)
        images_total = cursor.fetchone()[0]

        ImageEditText = DBRead('bw_config', 'text')

        cursor.close()
        cnx.close()
        return render_template('bwimage.html', data=[images_count, images_total, ImageEditText])

    else:
        return redirect(url_for("login"))


@app.route('/bw-image-results',methods=['POST'])
def BWResults():
    cnx = ms.connect(user='magic_register', password='Indira@2000',
                     host='185.104.29.84', database='magic_register')
    cursor = cnx.cursor()
    email = session['get_user_email']

    images_count_query = f"SELECT `images_count` FROM `user` WHERE `email` = '{email}'"
    cursor.execute(images_count_query)
    images_count = int(cursor.fetchone()[0])

    images_total_query = f"SELECT `images_total` FROM `user` WHERE `email` = '{email}'"
    cursor.execute(images_total_query)
    images_total = int(cursor.fetchone()[0])

    ImgFile = request.files['imageFile']
    cwd = os.getcwd()
    destination = os.path.join(cwd,ImgFile.filename)
    ImgFile.save(destination)
    print(ImgFile.filename)

    model = request.form.get('model')
    render_factor = request.form.get('render_factor')
    print("Working..")
    if images_count < images_total:
        # print(ImgPath)
        try:
            output = replicate.run("arielreplicate/deoldify_image:0da600fab0c45a66211339f1c16b71345d22f26ef5fea3dca1bb90bb5711e950",input={"input_image": open(ImgFile.filename,'rb+'),'model_name':model,'render_factor':int(render_factor)})
            print("Done")
            images_update_query = f"UPDATE `user` SET `images_count` = '{images_count+1}' WHERE `email` = '{email}';"
            cursor.execute(images_update_query)
            cnx.commit()
            cursor.close()
            cnx.close()
            os.remove(ImgFile.filename)
            return render_template('bwimage-results.html',data=[images_count+1,images_total,output,"",""])
        except Exception as e:
            print(e)
            return render_template('bwimage-results.html',data=[images_count,images_total,"","There's some problems in your image",""])
    else:
        return render_template('bwimage-results.html',data=[images_count,images_total,"","","You have used all your images"])




# Utility function for updating the form data to database
def DBUpdate(table, field, value):
    cnx = ms.connect(user='magic_register', password='Indira@2000',
                     host='185.104.29.84', database='magic_register')
    cursor = cnx.cursor()
    query = f"UPDATE `{table}` SET `{field}` = '{value}'"
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()


def DBRead(table, field):
    cnx = ms.connect(user='magic_register', password='Indira@2000',
                     host='185.104.29.84', database='magic_register')
    cursor = cnx.cursor(buffered=True)
    query = f"SELECT `{field}` FROM `{table}`"
    cursor.execute(query)
    data = cursor.fetchone()[0]
    cursor.close()
    cnx.close()
    return data


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(port=5000,host="0.0.0.0",debug=True)
