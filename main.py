from flask import Flask
from flask import Flask, render_template, request, redirect, url_for, session
from flask_nav import Nav
from flask_nav.elements import *
import db

#name the app
app = Flask(__name__)
app.secret_key='web_app_final'

@app.route('/', methods=['GET', 'POST'])
def index_foo():
    return redirect(url_for('index'))

#main page
@app.route('/index.html', methods=['GET', 'POST'])
def index():
    
    error1=''
    error2=''
    error3=''

    if request.method == 'POST':
        
        #customer login
        if request.form["myforms"]=="customer":
            login_attempt=db.get_login(db.get_connection(),request.form['cname'],request.form['cpass'])
            if(login_attempt != None):
                if(login_attempt['username']==request.form['cname'] and login_attempt['password']==request.form['cpass']):
                    #print("customer logged in")
                    session['loggedin']=True
                    session['username']=login_attempt['username']
                    return redirect(url_for('customer_home'))

            else:
                error1 = 'Invalid Credentials. Try again.'
        
        #employee login
        if request.form["myforms"]=="emp":
            login_attempt=db.get_login(db.get_connection(),request.form['ename'],request.form['epass'])
            if(login_attempt != None):
                if(login_attempt['username']==request.form['ename'] and login_attempt['password']==request.form['epass']):
                    print("employee logged in")
            else:
                error2 = 'Invalid Credentials. Try again.'
                    
        #admin login
        if request.form["myforms"]=="admin":
            login_attempt=db.get_login(db.get_connection(),request.form['aname'],request.form['apass'])
            if(login_attempt != None):
                if(login_attempt['username']==request.form['aname'] and login_attempt['password']==request.form['apass']):
                    print("admin logged in")
            else:
                error3 = 'Invalid Credentials. Try again.'
            
    return render_template('index.html',error1=error1,error2=error2,error3=error3)
   
@app.route('/customer.html', methods=['GET', 'POST'])
def customer_home():
    db.get_menu(db.get_connection())
    
    return render_template('customer.html',customer=session['username'])
    

if __name__ == '__main__':
    app.run()
