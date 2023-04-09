from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector as ms

cnx = ms.connect(user='magic_register', password='Indira@2000',
                 host='185.104.29.84',
                 database='magic_register')

cursor = cnx.cursor()


app = Flask(__name__)
app.secret_key = 'my-secret-key'

@app.route("/")
# @app.route("/login")
def login():
    return render_template('login.html')


@app.route("/",methods=['POST','GET'])

def Authenticate():
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

    if login_code != auth_code:
        return render_template("login.html",data="Incorrect Email or Password")
    else:
        return redirect(url_for('Dashboard'))

@app.route('/logout')
def logout():
    session.pop('get_user_email', None) # remove the email from the session
    return redirect(url_for('login'))


@app.route("/dashboard")
def Dashboard():
    if 'get_user_email' in session:
        email = session.get("get_user_email")
        # print(email)
        query = f"SELECT `name` FROM `user` WHERE `email` = '{email}'"
        cursor.execute(query)
        # Fetching the password from the database query
        password = cursor.fetchone()[0]
        # print(password)
        cnx.commit()
        return render_template("dashboard.html",data=password)

    else :
        return redirect(url_for("login"))




@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(port=5000)
