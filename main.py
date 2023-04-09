from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector as ms


app = Flask(__name__)
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
        return render_template("dashboard.html", data={'name': name, 'subscription_end': subscription_end, 'words_total': words_total, 'words_count': words_count, 'images_total':images_total, 'images_count':images_count})

    else:     
        return redirect(url_for("login"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server(e):
    return render_template('500.html'), 500



if __name__ == "__main__":
    app.run(port=5000)
