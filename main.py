from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from bwimage import BWImageAPI
from whisper import WhisperFileAPI, WhisperMICAPI
from image_edit import ImageEditAPI
from utitlities import DBRead, DBReadARG
from utitlities import custom_round
import os


app = Flask(__name__, static_url_path='/static')
app.secret_key = '5gfdfdsdr345dgfs45dgfdgdfg09043532%##$h2h340adsf9'



@app.route("/")
def login():
    return render_template('login.html')


@app.route("/", methods=['POST', 'GET'])
def Authenticate():
    email = request.form['email']
    login_code = request.form['login_code']

    # You can add code here to validate the user's login information
    auth_code = DBReadARG('user','pythonlogin','email',email)
    session['userSession'] = email
    if login_code != auth_code:
        return render_template("login.html", data="Incorrect Email or Password")
    else:
        return redirect(url_for('Dashboard'))


@app.route('/logout')
def logout():
    session.pop('userSession', None)  # remove the email from the session
    return redirect(url_for('login'))



@app.route("/dashboard")
def Dashboard():
    if 'userSession' in session:
        userSession = session.get('userSession')

        ########## Getting the User data using Email from database ###########
        name = DBReadARG('user','name','email',userSession)

        # Subscription Details
        subscription_end = DBReadARG('user','end_subscription_period','email',userSession)

        # Words Usage
        words_total = DBReadARG('user','words_total','email',userSession)
        words_count = DBReadARG('user','words_count','email',userSession)

        # Image Usage
        images_total = DBReadARG('user','images_total','email',userSession)
        images_count = DBReadARG('user','images_count','email',userSession)

        # Minutes Usage
        minutes_total = DBReadARG('user','minutes_total','email',userSession)
        minutes_count = DBReadARG('user','minutes_count','email',userSession)

        return render_template("dashboard.html", data={'name': name, 'subscription_end': subscription_end, 'words_total': words_total, 'words_count': words_count, 'images_total': images_total, 'images_count': images_count, 'minutes_total': minutes_total, 'minutes_count': minutes_count})
    
    else:
        return redirect(url_for("login"))
    

################Frontend to Backend Data Handling#######################


@app.route('/whisper-upload', methods=['POST'])
def whisper_upload():
    audioRecorded = request.files.get('audio')
    cwd = os.getcwd()
    destination = os.path.join(cwd,audioRecorded.filename)
    audioRecorded.save(destination)
    print(audioRecorded.filename)
    session['filename'] = audioRecorded.filename

    type = request.form.get('type')
    session['type'] = type
    
    duration = request.form.get('duration')
    session['duration'] = duration
    print(duration)
    return "Done"


@app.route('/whisper', methods=['POST', 'GET'])
def Whisper():
    if 'userSession' in session:
        userSession = session.get('userSession')

        minutes_total = DBReadARG('user','minutes_total','email',userSession)
        minutes_count = DBReadARG('user','minutes_count','email',userSession)
        WhisperAIText = DBRead('whisper_config', 'whisper_text')
        
        data = {
            'minutes_count':custom_round(float(minutes_count)),
            'minutes_total':minutes_total,
            'WhisperAIText':WhisperAIText,
            'warning': ""
        }
        return render_template('whisper.html', **data)

    else:
        return redirect(url_for("login"))


@app.route('/whisper-results', methods=["POST"])
def WhisperAI():
    userSession = session.get('userSession')
    filename = session.get('filename')
    duration = float(session.get('duration'))
    task = request.form.get('task')
    type = session.get('type')

    minutes_total = DBReadARG('user','minutes_total','email',userSession)
    minutes_count = DBReadARG('user','minutes_count','email',userSession)

    if (float(minutes_count) >= float(minutes_total)):
        print('inside if')
        data = {
            'minutes_count':custom_round(float(minutes_count)),
            'minutes_total':minutes_total,
            'WhisperAIText':'',
            'warning': "You Have Used All Your Minutes"
        }
        return render_template('whisper-results.html', **data)

    else:
        if (task == 'transcribe' and type == 'mic'):
            transcription, detected_language, minutes_to_update = WhisperMICAPI(filename,duration,userSession,task)
            return jsonify({'outputData': transcription, 'language_detect': detected_language, 'minutes_count': minutes_to_update, "minutes_total": minutes_total})

        elif (task == 'transcribe' and type == 'file'):
            transcription, detected_language, minutes_to_update = WhisperFileAPI(filename,duration,userSession,task)
            print(transcription,detected_language,minutes_to_update)
            return jsonify({'outputData': transcription, 'language_detect': detected_language, 'minutes_count': minutes_to_update, "minutes_total": minutes_total})
            
        elif (task == 'translate' and type == 'mic'):
            translate, detected_language, minutes_to_update = WhisperMICAPI(filename,duration,userSession,task)
            return jsonify({'translate': translate, 'language_detect': detected_language, 'minutes_count': minutes_to_update, "minutes_total": minutes_total})

        else:
            translate, detected_language, minutes_to_update = WhisperFileAPI(filename,duration,userSession,task)
            return jsonify({'translate': translate, 'language_detect': detected_language, 'minutes_count': minutes_to_update, "minutes_total": minutes_total})


@app.route('/upload-image',methods=['POST'])
def upload_image():
    imgFile = request.files.get('imageFile')
    cwd = os.getcwd()
    destination = os.path.join(cwd,imgFile.filename)
    imgFile.save(destination)
    print(imgFile.filename)
    session['imgFilename'] = imgFile.filename
    return "Uploaded Succesfully"


@app.route('/image-edit',methods=['GET','POST'])
def ImageEdit():
    if 'userSession' in session:
        userSession = session.get('userSession')

        images_total = DBReadARG('user','images_total','email',userSession)
        images_count = DBReadARG('user','images_count','email',userSession)
        ImageEditText = DBRead('image_edit_config', 'image_edit_text')

        data = {
            'images_count':images_count,
            'images_total':images_total,
            'ImageEditText':ImageEditText,
            'warning': ""
        }
        return render_template('imagedit.html', **data)

    else:
        return redirect(url_for("login"))


@app.route('/image-edit-results',methods=['POST'])
def ImageEditResults():
    userSession = session.get('userSession')
    imgFilename = session.get('imgFilename')
    user_prompt = request.form.get('prompt')
    user_neg_prompt = request.form.get('neg_prompt')
    user_output_images = int(request.form.get('output_images'))


    images_total = DBReadARG('user','images_total','email',userSession)
    images_count = DBReadARG('user','images_count','email',userSession)

    if (images_count <= images_total):
        data = {
            'images':'',
            'images_count':images_count,
            'images_total':images_total,
            'ImageEditText':'',
            'warning': "You Have Used All Your images"
        }
        os.remove(imgFilename)
        return render_template('imagedit-results.html', **data)
    
    else:
        output ,error, images_to_update =  ImageEditAPI(imgFilename, user_prompt, user_neg_prompt, user_output_images, userSession)
        data = {
            'images':output,
            'images_count':images_to_update,
            'images_total':images_total,
            'ImageEditText':'',
            'warning':'',
            'error':error
        }
        os.remove(imgFilename)
        return render_template('imagedit-results.html', **data)


@app.route('/upload-bw-image',methods=['POST'])
def upload_bw_image():
    imgbwFile = request.files.get('imageFile')
    cwd = os.getcwd()
    destination = os.path.join(cwd,imgbwFile.filename)
    imgbwFile.save(destination)
    print(imgbwFile.filename)
    session['imgbwFilename'] = imgbwFile.filename
    return "Uploaded Succesfully"


@app.route('/bw-image',methods=['GET','POST'])
def BWImage():
    if 'userSession' in session:
        userSession = session.get('userSession')

        images_total = DBReadARG('user','images_total','email',userSession)
        images_count = DBReadARG('user','images_count','email',userSession)
        BWEditText = DBRead('bw_config', 'text')

        data = {
            'images_count':images_count,
            'images_total':images_total,
            'BWEditText':BWEditText,
            'warning': ""
        }
        return render_template('bwimage.html', **data)
    
    else:
        return redirect(url_for("login"))


@app.route('/bw-image-results',methods=['POST','GET'])
def BWImageResults():
    userSession = session.get('userSession')
    imgbwFilename = session.get('imgbwFilename')
    model = request.form.get('model')
    renderFactor = request.form.get('render_factor')


    images_total = DBReadARG('user','images_total','email',userSession)
    images_count = DBReadARG('user','images_count','email',userSession)

    if (images_count <= images_total):
        data = {
            'images':'',
            'images_count':images_count,
            'images_total':images_total,
            'BWEditText':'',
            'warning': "You Have Used All Your images"
        }
        os.remove(imgbwFilename)
        return render_template('bwimage-results.html', **data)
    
    else:
        output, error, images_to_update = BWImageAPI(imgbwFilename,model,renderFactor,userSession)
        data = {
            'images':output,
            'images_count':images_to_update,
            'images_total':images_total,
            'BWEditText':'',
            'warning':'',
            'error':error
        }
        os.remove(imgbwFilename)
        return render_template('bwimage-results.html', **data)
        

@app.route('/chatgpt-4',methods=["GET",'POST'])
def ChatGPT():
    return render_template('chatgpt-4.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(port=5000,debug=True,host='0.0.0.0')
