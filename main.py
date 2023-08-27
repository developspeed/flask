from flask import Flask, render_template, request, redirect, session, url_for, jsonify, g 
from werkzeug.utils import secure_filename
from bwimage import BWImageAPI
from whisper import WhisperFileAPI, WhisperMICAPI
from image_edit import ImageEditAPI
from chatgpt import ChatGPTAPI
from dalleimage import DalleImageAPI
from dalleedit import DalleImageEditAPI
from dallevariation import DalleImageVariationAPI
from scribble import ScribbleAPI
from chatdocs import get_answer_for_question
from utitlities import DBRead, DBReadARG, DBUpdateARG, custom_round
import threading
import os
from ftplib import FTP
from pytube import YouTube
from datetime import datetime, date, timedelta 
from connection_cred import username, hostname, password, remote_file_path

app = Flask(__name__, static_url_path="/static")
app.secret_key = "5gfdfdsdr345dgfs45dgfdgdfg09043532%##$h2h340adsf9"
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/")
def login():
    return render_template("login.html")


@app.route("/", methods=["POST", "GET"])
def Authenticate():
    try:
        email = request.form["email"]
        login_code = request.form["login_code"]

        # You can add code here to validate the user's login information
        result = {}
        auth_code = DBReadARG("user", "pythonlogin", "email", email, result)
        session["userSession"] = email
        if login_code != auth_code or login_code == "" or email == "":
            return render_template("login.html", data="Incorrect Email or Password")
        else: 
            return redirect(url_for("Dashboard"))
    except Exception as e:
        return render_template('login.html')


@app.route("/logout")
def logout():
    session.pop("userSession", None)  # remove the email from the session
    return redirect(url_for("login"))


@app.route("/dashboard")
def Dashboard():
    if "userSession" in session:
        userSession = session.get("userSession")

        ########## Getting the User data using Email from database ###########
        result = {}

        name_task = threading.Thread(
            target=DBReadARG, args=("user", "name", "email", userSession, result)
        )
        end_subscription_period = threading.Thread(
            target=DBReadARG,
            args=("user", "end_subscription_period", "email", userSession, result),
        ) 
        subscription_start_task = threading.Thread(
            target=DBReadARG,
            args=("user", "subscription_start_date", "email", userSession, result),
        )
        words_total_task = threading.Thread(
            target=DBReadARG, args=("user", "words_total", "email", userSession, result)
        )
        words_count_task = threading.Thread(
            target=DBReadARG, args=("user", "words_count", "email", userSession, result)
        )
        images_total_task = threading.Thread(
            target=DBReadARG,
            args=("user", "images_total", "email", userSession, result),
        )
        images_count_task = threading.Thread(
            target=DBReadARG,
            args=("user", "images_count", "email", userSession, result),
        )
        minutes_total_task = threading.Thread(
            target=DBReadARG,
            args=("user", "minutes_total", "email", userSession, result),
        )
        minutes_count_task = threading.Thread(
            target=DBReadARG,
            args=("user", "minutes_count", "email", userSession, result),
        )
        whisper = threading.Thread(
            target=DBReadARG, args=("user", "whisper", "email", userSession, result)
        )
        edit_image = threading.Thread(
            target=DBReadARG, args=("user", "edit_image", "email", userSession, result)
        )
        bw_tocolor = threading.Thread(
            target=DBReadARG, args=("user", "bw_tocolor", "email", userSession, result)
        )
        chatgpt = threading.Thread(
            target=DBReadARG,
            args=("user", "create_content", "email", userSession, result),
        )
        dalle = threading.Thread(
            target=DBReadARG,
            args=("user", "create_image", "email", userSession, result),
        )
        scribble = threading.Thread(
            target=DBReadARG,
            args=("user", "scribble", "email", userSession, result),
        )

        # Start the task
        name_task.start()
        end_subscription_period.start()
        subscription_start_task.start()
        words_total_task.start()
        words_count_task.start()
        images_total_task.start()
        images_count_task.start()
        minutes_total_task.start()
        minutes_count_task.start()
        whisper.start()
        edit_image.start()
        bw_tocolor.start()
        chatgpt.start()
        dalle.start()
        scribble.start()

        # Join the task
        name_task.join()
        end_subscription_period.join()
        subscription_start_task.join()
        words_total_task.join()
        words_count_task.join()
        images_total_task.join()
        images_count_task.join()
        minutes_total_task.join()
        minutes_count_task.join()
        whisper.join()
        edit_image.join()
        bw_tocolor.join()
        chatgpt.join()
        dalle.join()
        scribble.join()
        
        # User Name
        name = result["name"]

        # Subscription Details
        subscription_start = result['subscription_start_date']
        subscription_end = result["end_subscription_period"]

        # Words Usage
        words_total = result["words_total"]
        words_count = result["words_count"]

        # Image Usage
        images_total = result["images_total"]
        images_count = result["images_count"]

        # Minutes Usage
        minutes_total = result["minutes_total"]
        minutes_count = result["minutes_count"]

        # State Check
        whisper_state = result["whisper"]
        edit_image_state = result["edit_image"]
        bw_tocolor_state = result["bw_tocolor"]
        create_content_state = result["create_content"]
        dalle_state = result['create_image']
        scribble_state = result['scribble']

        # If someone is new user and haven't got susbscription yet then he has 10 days from today after that he will not able to use the api
        if(subscription_start == None):
            date_first_login_query = DBReadARG('user','date_first_login','email',userSession,result)
            date_first_login = result['date_first_login']
            subscription_end = date_first_login + timedelta(days=10)
                
        

        # Date Calculation
        year = int(str(subscription_end)[:4])
        month = int(str(subscription_end)[5:7])
        dates = int(str(subscription_end)[8:11])

        curYear = int(datetime.now().year)
        curMonth = int(datetime.now().month)
        curdate = int(datetime.now().day)

        flag = 0
        if dates - curdate <= 8 and month - curMonth == 0 and year - curYear == 0:
            flag = 1    

        return render_template(
            "dashboard.html",
            data={
                "name": name,
                "subscription_end": subscription_end,
                "words_total": words_total,
                "words_count": words_count,
                "images_total": images_total,
                "images_count": images_count,
                "minutes_total": minutes_total,
                "minutes_count": minutes_count,
                "whisper_state": whisper_state,
                "edit_image_state": edit_image_state,
                "bw_tocolor_state": bw_tocolor_state,
                "create_content_state": create_content_state,
                "create_image_state": dalle_state,
                "scribble_state":scribble_state,
                "flag": flag
            },
        )

    else:
        return redirect(url_for("login"))

@app.route('/userFilesUpload',methods=["POST"])
def UserFileUpload():
    userFile = request.files.get('userFiles');
    localfile = userFile.filename
    ftp = FTP(hostname)
    ftp.login(username, password)

    try:
        # Upload the file to the FTP server
        ftp.storbinary('STOR ' +localfile, userFile)

        # Generate the link to the uploaded file
        file_link = 'https://www.magicaibox.site/doc/'+ localfile

        return file_link
    
    except Exception as e:
        return 'Error: ' + str(e)
    
    finally:
        # Close the FTP connection
        ftp.quit()

################Frontend to Backend Data Handling#######################


########################################### Whisper AI ###############################################

@app.route("/whisper-upload", methods=["POST"])
def whisper_upload():
    if request.files.get("audio") != None:
        audioRecorded = request.files.get("audio")
        cwd = os.getcwd()
        destination = os.path.join(cwd, audioRecorded.filename)
        audioRecorded.save(destination)

        session["filename"] = audioRecorded.filename

        type = request.form.get("type")
        session["type"] = type

        duration = request.form.get("duration")
        session["duration"] = duration
        return "Done"
    else:
        ytLink = request.form.get('ytLink')
        yt = YouTube(ytLink)
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download(output_path='')
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        session['filename'] = new_file

        type = request.form.get("type")
        session["type"] = type

        # duration    
        session["duration"] = yt.length/60

        return "YT DONE"


@app.route("/whisper", methods=["POST", "GET"])
def Whisper():
    if "userSession" in session:
        userSession = session.get("userSession")
        result = {}
        minutes_total_task = threading.Thread(
            target=DBReadARG,
            args=("user", "minutes_total", "email", userSession, result),
        )
        minutes_count_task = threading.Thread(
            target=DBReadARG,
            args=("user", "minutes_count", "email", userSession, result),
        )
        WhisperAIText = DBRead("whisper_config", "whisper_text")

        minutes_total_task.start()
        minutes_count_task.start()

        minutes_total_task.join()
        minutes_count_task.join()

        # Minutes Usage
        minutes_total = result["minutes_total"]
        minutes_count = result["minutes_count"]

        data = {
            "minutes_count": custom_round(float(minutes_count)),
            "minutes_total": minutes_total,
            "WhisperAIText": WhisperAIText,
            "warning": "",
        }
        return render_template("whisper.html", **data)

    else:
        return redirect(url_for("login"))


@app.route("/whisper-results", methods=["POST"])
def WhisperAI():
    userSession = session.get("userSession")
    filename = session.get("filename")
    duration = float(session.get("duration"))
    task = request.form.get("task")
    type = session.get("type")

    result = {}
    minutes_total_task = threading.Thread(
        target=DBReadARG, args=("user", "minutes_total", "email", userSession, result)
    )
    minutes_count_task = threading.Thread(
        target=DBReadARG, args=("user", "minutes_count", "email", userSession, result)
    )

    minutes_total_task.start()
    minutes_count_task.start()

    minutes_total_task.join()
    minutes_count_task.join()

    # Minutes Usage
    minutes_total = result["minutes_total"]
    minutes_count = result["minutes_count"]

    if float(minutes_count) >= float(minutes_total):
        return jsonify(
            {
                "outputData": "You Have Used All Your Minutes",
                "minutes_count": minutes_count,
                "minutes_total": minutes_total,
            }
        )

    else:
        if task == "transcribe" and type == "mic":
            transcription, detected_language, minutes_to_update = WhisperMICAPI(
                filename, duration, userSession, task
            )
            return jsonify(
                {
                    "outputData": transcription,
                    "language_detect": detected_language,
                    "minutes_count": minutes_to_update,
                    "minutes_total": minutes_total,
                }
            )

        elif task == "transcribe" and type == "file":
            transcription, detected_language, minutes_to_update = WhisperFileAPI(
                filename, duration, userSession, task
            )
        
            return jsonify(
                {
                    "outputData": transcription,
                    "language_detect": detected_language,
                    "minutes_count": minutes_to_update,
                    "minutes_total": minutes_total,
                }
            )

        elif task == "translate" and type == "mic":
            translate, detected_language, minutes_to_update = WhisperMICAPI(
                filename, duration, userSession, task
            )
            return jsonify(
                {
                    "translate": translate,
                    "language_detect": detected_language,
                    "minutes_count": minutes_to_update,
                    "minutes_total": minutes_total,
                }
            )

        else:
            translate, detected_language, minutes_to_update = WhisperFileAPI(
                filename, duration, userSession, task
            )
            # os.remove(filename)
            return jsonify(
                {
                    "translate": translate,
                    "language_detect": detected_language,
                    "minutes_count": minutes_to_update,
                    "minutes_total": minutes_total,
                }
            )

############################################ Edit Image ############################################

@app.route("/upload-image", methods=["POST"])
def upload_image():
    imgFile = request.files.get("imageFile")
    cwd = os.getcwd()
    destination = os.path.join(cwd, imgFile.filename)
    imgFile.save(destination)
    session["imgFilename"] = imgFile.filename
    return "Uploaded Succesfully"


@app.route("/image-edit", methods=["GET", "POST"])
def ImageEdit():
    if "userSession" in session:
        userSession = session.get("userSession")

        result = {}
        images_total_task = threading.Thread(
            target=DBReadARG,
            args=("user", "images_total", "email", userSession, result),
        )
        images_count_task = threading.Thread(
            target=DBReadARG,
            args=("user", "images_count", "email", userSession, result),
        )
        ImageEditText = DBRead("image_edit_config", "image_edit_text")

        images_total_task.start()
        images_count_task.start()

        images_total_task.join()
        images_count_task.join()

        images_total = result["images_total"]
        images_count = result["images_count"]

        data = {
            "images_count": images_count,
            "images_total": images_total,
            "ImageEditText": ImageEditText,
            "warning": "",
        }
        return render_template("imagedit.html", **data)

    else:
        return redirect(url_for("login"))


@app.route("/image-edit-results", methods=["POST"])
def ImageEditResults():
    userSession = session.get("userSession")
    imgFilename = session.get("imgFilename")
    user_prompt = request.form.get("prompt")
    user_neg_prompt = request.form.get("neg_prompt")
    user_output_images = int(request.form.get("output_images"))

    result = {}
    images_total_task = threading.Thread(
        target=DBReadARG, args=("user", "images_total", "email", userSession, result)
    )
    images_count_task = threading.Thread(
        target=DBReadARG, args=("user", "images_count", "email", userSession, result)
    )

    images_total_task.start()
    images_count_task.start()

    images_total_task.join()
    images_count_task.join()

    images_total = result["images_total"]
    images_count = result["images_count"]

    if int(images_count) >= int(images_total):
        data = {
            "images": "",
            "images_count": images_count,
            "images_total": images_total,
            "ImageEditText": "",
            "warning": "You Have Used All Your images",
        }
        os.remove(imgFilename)
        return render_template("imagedit-results.html", **data)

    else:
        output, error, images_to_update = ImageEditAPI(
            imgFilename, user_prompt, user_neg_prompt, user_output_images, userSession
        )
        data = {
            "images": output,
            "images_count": images_to_update,
            "images_total": images_total,
            "ImageEditText": "",
            "warning": "",
            "error": error,
        }
        os.remove(imgFilename)
        return render_template("imagedit-results.html", **data)


########################################### BW Image #####################################################

@app.route("/upload-bw-image", methods=["POST"])
def upload_bw_image():
    imgbwFile = request.files.get("imageFile")
    cwd = os.getcwd()
    destination = os.path.join(cwd, imgbwFile.filename)
    imgbwFile.save(destination)
    session["imgbwFilename"] = imgbwFile.filename
    return "Uploaded Succesfully"


@app.route("/bw-image", methods=["GET", "POST"])
def BWImage():
    if "userSession" in session:
        userSession = session.get("userSession")
        result = {}
        images_total_task = threading.Thread(
            target=DBReadARG,
            args=("user", "images_total", "email", userSession, result),
        )
        images_count_task = threading.Thread(
            target=DBReadARG,
            args=("user", "images_count", "email", userSession, result),
        )
        BWEditText = DBRead("bw_config", "text")

        images_total_task.start()
        images_count_task.start()

        images_total_task.join()
        images_count_task.join()

        images_total = result["images_total"]
        images_count = result["images_count"]

        data = {
            "images_count": images_count,
            "images_total": images_total,
            "BWEditText": BWEditText,
            "warning": "",
        }
        return render_template("bwimage.html", **data)

    else:
        return redirect(url_for("login"))


@app.route("/bw-image-results", methods=["POST", "GET"])
def BWImageResults():
    userSession = session.get("userSession")
    imgbwFilename = session.get("imgbwFilename")
    model = request.form.get("model")
    renderFactor = request.form.get("render_factor")

    result = {}
    images_total_task = threading.Thread(
        target=DBReadARG, args=("user", "images_total", "email", userSession, result)
    )
    images_count_task = threading.Thread(
        target=DBReadARG, args=("user", "images_count", "email", userSession, result)
    )

    images_total_task.start()
    images_count_task.start()

    images_total_task.join()
    images_count_task.join()

    images_total = result["images_total"]
    images_count = result["images_count"]

    if int(images_count) >= int(images_total):
        data = {
            "images": "",
            "images_count": images_count,
            "images_total": images_total,
            "BWEditText": "",
            "warning": "You Have Used All Your images",
        }
        os.remove(imgbwFilename)
        return render_template("bwimage-results.html", **data)

    else:
        output, error, images_to_update = BWImageAPI(
            imgbwFilename, model, renderFactor, userSession
        )
        data = {
            "images": output,
            "images_count": images_to_update,
            "images_total": images_total,
            "BWEditText": "",
            "warning": "",
            "error": error,
        }
        os.remove(imgbwFilename)
        return render_template("bwimage-results.html", **data)


####################################### Scribble Image ###################################

@app.route('/scribble-upload', methods=['POST'])
def upload_scribble():
    image = request.files['image']  # Get the uploaded image from the request
    session['scribbleImage'] = (image.filename)
    session['scribblePrompt'] = request.form['prompt']

    cwd = os.getcwd()
    destination = os.path.join(cwd, image.filename)
    image.save(destination)
    # For demonstration purposes, let's just return the received data as JSON
    return jsonify({'prompt': session['scribbleImage'], 'success': True}), 200
    


@app.route("/scribble",methods=['GET','POST'])
def Scribble():
    if 'userSession' in session:
        userSession = session.get('userSession')
        result = {}
        images_total_task = threading.Thread(target=DBReadARG,args=("user", "images_total", "email", userSession, result))
        images_count_task = threading.Thread(target=DBReadARG,args=("user", "images_count", "email", userSession, result))
        ScribbleText = DBRead("scribble", "scribble_text")

        images_total_task.start()
        images_count_task.start()

        images_total_task.join()
        images_count_task.join()

        images_total = result["images_total"]
        images_count = result["images_count"]

        data = {
            "images_count": images_count,
            "images_total": images_total,
            "ScribbleText": ScribbleText,
            "warning": "",
        }
        
        return render_template('scribble.html', **data)
    else:
        return redirect(url_for('login'))


@app.route('/scribble-results',methods=['POST'])
def ScribblResults():
    userSession = session.get('userSession')
    scribbleImage = session.get('scribbleImage')
    scribblePrompt = session.get('scribblePrompt')

    result = {}
    images_total_task = threading.Thread(
        target=DBReadARG, args=("user", "images_total", "email", userSession, result)
    )
    images_count_task = threading.Thread(
        target=DBReadARG, args=("user", "images_count", "email", userSession, result)
    )

    images_total_task.start()
    images_count_task.start()

    images_total_task.join()
    images_count_task.join()

    images_total = result["images_total"]
    images_count = result["images_count"] 

    if int(images_count) >= int(images_total):
        data = {
            "images": "",
            "images_count": images_count,
            "images_total": images_total,
            "ScribbleText": "",
            "warning": "You Have Used All Your images",
        }
        session.pop("scribbleImage",None)
        session.pop("scribblePrompt",None)
        os.remove(scribbleImage)
        return render_template("scribble-results.html", **data)

    else:
        output, error, images_to_update = ScribbleAPI(scribbleImage,scribblePrompt,userSession)
        data = {
            "images": output,
            "images_count": images_to_update,
            "images_total": images_total,
            "ScribbleText": "",
            "warning": "",
            "error": error,
        }
        session.pop("scribbleImage",None)
        session.pop("scribblePrompt",None)
        os.remove(scribbleImage)
        return render_template("scribble-results.html", **data)

####################################### ChatGPT-4 ########################################


@app.route("/chatgpt-4", methods=["GET", "POST"])
def ChatGPT():
    if "userSession" in session:
        userSession = session.get("userSession")

        result = {}
        words_total_task = threading.Thread(
            target=DBReadARG, args=("user", "words_total", "email", userSession, result)
        )
        words_count_task = threading.Thread(
            target=DBReadARG, args=("user", "words_count", "email", userSession, result)
        )
        ChatGPTText = DBRead("chatgpt-4", "chat_gpt_text")

        words_total_task.start()
        words_count_task.start()

        words_total_task.join()
        words_count_task.join()

        words_total = result["words_total"]
        words_count = result["words_count"]

        data = {
            "words_total": words_total,
            "words_count": words_count,
            "ChatGPTText": ChatGPTText,
            "warning": "",
        }

        return render_template("chatgpt-4.html", **data)

    else:
        return redirect(url_for("login"))


@app.route("/chatgpt-results", methods=["POST", "GET"])
def ChatGPTResults():
    userSession = session.get("userSession")
    prompts = request.form.get("prompt")

    result = {}
    words_total_task = threading.Thread(
        target=DBReadARG, args=("user", "words_total", "email", userSession, result)
    )
    words_count_task = threading.Thread(
        target=DBReadARG, args=("user", "words_count", "email", userSession, result)
    )

    words_total_task.start()
    words_count_task.start()

    words_total_task.join()
    words_count_task.join()

    words_total = result["words_total"]
    words_count = result["words_count"]

    if int(words_count) >= int(words_total):
        ChatGPTText = DBRead("chatgpt-4", "chat_gpt_text")
        data = {
            "words_total": words_total,
            "words_count": words_count,
            "ChatGPTText": ChatGPTText,
            "warning": "You have used all your words",
        }

        return render_template("chatgpt-4.html", **data)
    else:
        output, words_to_update = ChatGPTAPI(prompts, userSession)
        return jsonify(
            {
                "output": output,
                "words_count": words_to_update,
                "words_total": words_total,
                "warning": "",
            }
        )


####################################### Dalle Images #######################################

@app.route('/dalle-images-upload',methods=['POST'])
def DalleImageUpload():
    dalleimage = request.files.get("imageFile")
    cwd = os.getcwd()
    destination = os.path.join(cwd, dalleimage.filename)
    dalleimage.save(destination)

    session["dalleimage"] = dalleimage.filename
    return "Uploaded Succesfully"


@app.route('/dalle-image',methods=['GET','POST'])
def DalleImageGenerator():
    if "userSession" in session:
        userSession = session.get("userSession")
        result = {}
        images_total_task = threading.Thread(target=DBReadARG,args=("user", "images_total", "email", userSession, result))
        images_count_task = threading.Thread(target=DBReadARG,args=("user", "images_count", "email", userSession, result))
        DalleText = DBRead("dalle_image_generator", "dalle_image_text")

        images_total_task.start()
        images_count_task.start()

        images_total_task.join()
        images_count_task.join()

        images_total = result["images_total"]
        images_count = result["images_count"]

        data = {
            "images_count": images_count,
            "images_total": images_total,
            "DalleText": DalleText,
            "warning": "",
        }
        
        return render_template('dalleimage.html', **data)
    else:
        return redirect(url_for('login'))
    

@app.route('/dalle-results',methods=['POST','GET'])
def DalleImageResults():
    userSession = session.get("userSession")
    prompts = request.form['prompt']
    numImages = request.form['numImages']
    sizes = request.form['sizes']


    result = {}
    images_total_task = threading.Thread(
        target=DBReadARG, args=("user", "images_total", "email", userSession, result)
    )
    images_count_task = threading.Thread(
        target=DBReadARG, args=("user", "images_count", "email", userSession, result)
    )

    images_total_task.start()
    images_count_task.start()

    images_total_task.join()
    images_count_task.join()

    images_total = result["images_total"]
    images_count = result["images_count"]

    if int(images_count) >= int(images_total):
        data = {
            'images': "",
            "images_count": images_count,
            "images_total": images_total,
            "warning": "You Have Used All Your images",
        }
        return render_template('dalle-results.html', **data)

    else:
        images, updatedImage = DalleImageAPI(prompts,numImages,sizes,userSession)
        data = {
            'images':images,
            'images_count':updatedImage,
            'images_total':images_total,
            'warning':""
        }
        return render_template('dalle-results.html', **data)



@app.route('/dalle-edit', methods=['GET','POST'])
def DalleImageEdit():
    userSession = session.get("userSession")
    # get the image and save it 
    imageedit = request.files['editImageFile']
    cwd = os.getcwd()
    destination = os.path.join(cwd, imageedit.filename)
    imageedit.save(destination)
    session["imageedit"] = imageedit.filename


    prompts = request.form['prompt']
    numImages = request.form['numImages']
    sizes = request.form['sizes']

    result = {}
    images_total_task = threading.Thread(
        target=DBReadARG, args=("user", "images_total", "email", userSession, result)
    )
    images_count_task = threading.Thread(
        target=DBReadARG, args=("user", "images_count", "email", userSession, result)
    )

    images_total_task.start()
    images_count_task.start()

    images_total_task.join()
    images_count_task.join()

    images_total = result["images_total"]
    images_count = result["images_count"]


    if int(images_count) >= int(images_total):
        data = {
            'images': "",
            "images_count": images_count,
            "images_total": images_total,
            "warning": "You Have Used All Your images",
        }
        return render_template('dalle-results.html', **data)

    else:
        images, updatedImage = DalleImageEditAPI(session.get('imageedit'),prompts,numImages,sizes,userSession)
        data = {
            'images':images,
            'images_count':updatedImage,
            'images_total':images_total,
            'warning':""
        }
        os.remove(session.get('imageedit'))
        return render_template('dalle-results.html', **data)


@app.route('/dalle-variation', methods=['GET','POST'])
def DalleImageVariation():
    userSession = session.get("userSession")
    # get the image and save it 
    variationImageFile = request.files['variationImageFile']
    cwd = os.getcwd()
    destination = os.path.join(cwd, variationImageFile.filename)
    variationImageFile.save(destination)
    session["variationImageFile"] = variationImageFile.filename

    numImages = request.form['numImages']
    sizes = request.form['sizes']

    result = {}
    images_total_task = threading.Thread(
        target=DBReadARG, args=("user", "images_total", "email", userSession, result)
    )
    images_count_task = threading.Thread(
        target=DBReadARG, args=("user", "images_count", "email", userSession, result)
    )

    images_total_task.start()
    images_count_task.start()

    images_total_task.join()
    images_count_task.join()

    images_total = result["images_total"]
    images_count = result["images_count"]

    if int(images_count) >= int(images_total):
        data = {
            'images': "",
            "images_count": images_count,
            "images_total": images_total,
            "warning": "You Have Used All Your images",
        }
        return render_template('dalle-results.html', **data)

    else:
        images, updatedImage = DalleImageVariationAPI(session.get('variationImageFile'),numImages,sizes,userSession)
        data = {
            'images':images,
            'images_count':updatedImage,
            'images_total':images_total,
            'warning':""
        }
        os.remove(session.get('variationImageFile'))
        return render_template('dalle-results.html', **data)


######################## ChatDocs ###########################

# Set the main upload folder
UPLOAD_FOLDER = 'documents'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create user-specific upload folder
@app.before_request
def before_request():
    g.userSession = session.get("userSession")
    if g.userSession:
        g.user_upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], g.userSession)
        if not os.path.exists(g.user_upload_folder):
            os.makedirs(g.user_upload_folder)

@app.route('/upload', methods=['POST'])
def upload_files():
    uploaded_files = request.files.getlist('files')
    uploaded_filenames = []

    for file in uploaded_files:
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(g.user_upload_folder, filename)
            file.save(file_path)
            uploaded_filenames.append(filename)

    return jsonify({'message': 'Successfully Uploaded'})

@app.route('/delete_files', methods=['POST'])
def delete_files():
    # Delete all uploaded files in the user's folder
    indexFile = f'index_{g.userSession}.json'
    os.remove(indexFile)
    user_folder_path = os.path.join(app.config['UPLOAD_FOLDER'], g.userSession) 
    if os.path.exists(user_folder_path):
        for filename in os.listdir(user_folder_path):
            file_path = os.path.join(user_folder_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        
        return jsonify({'message': 'Successfully Deleted'})
    else:
        return jsonify({'message': 'User folder not found'})
    

@app.route('/chatdocs',methods=['GET','POST'])
def ChatDocs():
    if "userSession" in session:
        if request.method == 'GET':
            return render_template("chatdocs.html")
        elif request.method == 'POST':
            userSession = session.get('userSession')
            question = request.form.get('userMessage')
            # Process user_message and generate server_response
            response = get_answer_for_question(question,userSession)
            if response == 'null':
                return jsonify({'response': 'First upload the documents!'})
            return jsonify({'response': response})
    else:
        return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0",debug=True)
