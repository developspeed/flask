from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector as ms
import os
import replicate
from io import BytesIO


# Setting the Environment of the application using the API token of Replicate from the database
cnx = ms.connect(user='magic_register', password='Indira@2000',
                 host='185.104.29.84', database='magic_register')
cursor = cnx.cursor()
get_API_key_query = "SELECT `API_KEY` FROM `whisper_config`"
cursor.execute(get_API_key_query)
get_API_key = ''
for apiKEY in cursor:
    get_API_key = apiKEY[0]
# print(get_API_key)
os.environ['REPLICATE_API_TOKEN'] = str(get_API_key)

# Closing the DB Connection
cursor.close()
cnx.close()

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'my-secret-key'


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

    auth_code = ""
    for codes in cursor:
        for code in codes:
            auth_code = code

    # cnx.commit()
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

        cursor.close()
        cnx.close()
        return render_template("dashboard.html", data={'name': name, 'subscription_end': subscription_end, 'words_total': words_total, 'words_count': words_count, 'images_total': images_total, 'images_count': images_count, 'minutes_total':minutes_total, 'minutes_count':minutes_count})

    else:
        return redirect(url_for("login"))


minutes_count = 0
minutes_total = 0


@app.route('/whisper')
def Whisper():
    if 'get_user_email' in session:
        cnx = ms.connect(user='magic_register', password='Indira@2000',
                         host='185.104.29.84', database='magic_register')
        cursor = cnx.cursor()

        global minutes_count, minutes_total
        email = session['get_user_email']
        minutes_count_query = f"SELECT `minutes_count` FROM `user` WHERE `email` = '{email}'"
        cursor.execute(minutes_count_query)
        minutes_count = float(cursor.fetchone()[0])

        minutes_total_query = f"SELECT `minutes_total` FROM `user` WHERE `email` = '{email}'"
        cursor.execute(minutes_total_query)
        minutes_total = cursor.fetchone()[0]

        cursor.close()
        cnx.close()
        return render_template('whisper.html', data=[minutes_count, minutes_total])

    else:
        return redirect(url_for("login"))


audioRecordedGlobal = None
# Audio Upload through Mic


@app.route('/upload', methods=['POST'])
def upload():
    audio = request.files.get('audio').read()
    # print(audio)
    global audioRecordedGlobal
    audioRecordedGlobal = audio
    return "Done"


# function to convert the information into
# some readable format
def audio_duration(length):
    hours = length / 3600  # calculate in hours
    length %= 3600
    mins = length / 60  # calculate in minutes
    length %= 60
    seconds = length  # calculate in seconds

    return mins  # returns the duration


@app.route('/whisper-results', methods=["POST"])
def WhisperAI():
    cnx = ms.connect(user='magic_register', password='Indira@2000',
                     host='185.104.29.84', database='magic_register')
    cursor = cnx.cursor()
    email = session['get_user_email']
    # Reading the audio file and Converting the audio file in Bytes

    audioFile = BytesIO(request.files['audioFile'].read())
    # Or
    # Taking mic input
    audioRecords = BytesIO(audioRecordedGlobal)
    # print(audioRecordedGlobal)

    language = request.form['language']
    to_translate = request.form.get('to_translate') == 'on'

    if minutes_count <= float(minutes_total):
        if len(audioFile.read()) != 0:

            # Counting audio file minutes
            from mutagen.wave import WAVE
            audios = WAVE(audioFile)
            audio_length = audios.info.length
            minutes = str(audio_duration(audio_length))
            minutes_to_update = float(minutes[0:4])
            print(minutes_to_update)

            update_minutes_query = f"UPDATE `user` SET `minutes_count` = '{minutes_to_update+minutes_count}' WHERE `email` = '{email}';"
            cursor.execute(update_minutes_query)

            # Model Running
            output = replicate.run("openai/whisper:e39e354773466b955265e969568deb7da217804d8e771ea8c9cd0cef6591f8bc",
                                   input={"audio": audioFile,
                                          "model": "large-v2",
                                          "transcription": "plain text",
                                          "translate": to_translate,
                                          #   "language": language,
                                          "temperature": 0,
                                          #   "patience": 1.0,
                                          "suppress_tokens": "-1",
                                          "initial_prompt": "",
                                          "condition_on_previous_text": False,
                                          "temperature_increment_on_fallback": 0.2,
                                          "compression_ratio_threshold": 2.4,
                                          "logprob_threshold": -1,
                                          "no_speech_threshold": 0.6})

            cnx.commit()
            cursor.close()
            cnx.close()
            return render_template('whisper-results.html', data=[output['transcription'], output['translation'], output['detected_language'], minutes_count, minutes_total])

        else:
            # Counting audio file minutes
            # from mutagen.wave import WAVE

            # audios = WAVE(audioRecordedGlobal)
            # audio_length = audios.info.length
            # minutes = str(audio_duration(audio_length))
            # minutes_to_update = float(minutes[0:4])

            # update_minutes_query = f"UPDATE `user` SET `minutes_count` = '{minutes_to_update+minutes_count}' WHERE `email` = {email};"
            # cursor.execute(update_minutes_query)

            # Model Running
            output = replicate.run("openai/whisper:e39e354773466b955265e969568deb7da217804d8e771ea8c9cd0cef6591f8bc",
                                   input={"audio": audioRecords,
                                          "model": "large-v2",
                                          "transcription": "plain text",
                                          "translate": to_translate,
                                          #   "language": language,
                                          "temperature": 0,
                                          #   "patience": 1.0,
                                          "suppress_tokens": "-1",
                                          "initial_prompt": "",
                                          "condition_on_previous_text": False,
                                          "temperature_increment_on_fallback": 0.2,
                                          "compression_ratio_threshold": 2.4,
                                          "logprob_threshold": -1,
                                          "no_speech_threshold": 0.6})

            cnx.commit()
            cursor.close()
            cnx.close()
            return render_template('whisper-results.html', data=[output['transcription'], output['translation'], output['detected_language'], minutes_count, minutes_total])
            return "Done"
    else:
        return render_template('whisper-results.html', data=["", "", "", "", "", "You Have Used All Your Minutes"])


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(port=5000)
