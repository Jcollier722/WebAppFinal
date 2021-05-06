from flask import Flask
from flask import Flask, render_template, request, redirect, url_for, session,jsonify
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
                    session['loggedin']=True
                    session['username']=login_attempt['username']
                    return redirect(url_for('employee_home'))
            else:
                error2 = 'Invalid Credentials. Try again.'
        """            
        #admin login
        if request.form["myforms"]=="admin":
            login_attempt=db.get_login(db.get_connection(),request.form['aname'],request.form['apass'])
            if(login_attempt != None):
                if(login_attempt['username']==request.form['aname'] and login_attempt['password']==request.form['apass']):
                    print("admin logged in")
            else:
                error3 = 'Invalid Credentials. Try again.'
        """ 
    return render_template('index.html',error1=error1,error2=error2,error3=error3)
   
@app.route('/customer.html', methods=['GET', 'POST'])
def customer_home():
    menu = db.get_menu(db.get_connection())

    combos = menu[0]
    pizzas = menu[1]
    sides  = menu[2]
    subs   = menu[3]

    if request.method == 'POST':
        if request.form["myforms"]=="order":
            db.send_order(db.get_connection(),request.form['this_order'])
            
            order = request.form['this_order']
            subtotal = request.form['this_sub']
            tax = request.form['this_tax']

            total=(float(subtotal)+float(tax))

            session['order']=order
            session['subtotal']=subtotal
            session['tax']=tax
            session['total']=total
            
            return redirect(url_for('thank_cus'))
            
  
    return render_template('customer.html',
                           customer=session['username'],
                           combos=combos,
                           pizzas=pizzas,
                           sides=sides,
                           subs=subs)

@app.route('/thanks.html', methods=['GET', 'POST'])
def thank_cus():
    order = session['order']
    order_list= order.split(':')
    return render_template('thanks.html',order=order_list,subtotal=session['subtotal'],tax=session['tax'],total = session['total'])


@app.route('/employee.html', methods=['GET', 'POST'])
def employee_home():
    orders = db.get_orders(db.get_connection())

    if request.method == 'POST':
        if request.form["myforms"]=="complete_order":
            db.finish_order(db.get_connection(),request.form['order_id'])
            return redirect(url_for('employee_home'))

        if request.form["myforms"]=="add_menu":
            item_type = request.form['type']
            
            if(item_type == "combo"):
                db.add_combo(db.get_connection(),request.form['item'],request.form['price'])
            if(item_type == "pizza"):
                db.add_pizza(db.get_connection(),request.form['item'],request.form['price'])
            if(item_type == "side"):
                db.add_side(db.get_connection(),request.form['item'],request.form['price'])
            if(item_type == "subs"):
                db.add_sub(db.get_connection(),request.form['item'],request.form['price'])

        if request.form["myforms"]=="rem_menu":

            item_type = request.form['type_id']
            
            if(item_type == "combo"):
                db.delete_combo(db.get_connection(),request.form['item_id'])
            if(item_type == "pizza"):
                db.delete_pizza(db.get_connection(),request.form['item_id'])
            if(item_type == "side"):
                db.delete_side(db.get_connection(),request.form['item_id'])
            if(item_type == "subs"):
                db.delete_sub(db.get_connection(),request.form['item_id'])
        
    return render_template('employee.html',employee=session['username'],orders=orders)

@app.route('/register.html', methods=['GET', 'POST'])
def register_user():
    reg = ''
    if request.method == 'POST':
        if request.form["myforms"]=="register":
            uname = request.form['cname']
            upass = request.form['cpass']
            first = request.form['fname']
            last = request.form['lname']
            addr = request.form['addr']
            pay = request.form['pay']

            reg_s = db.register_customer(db.get_connection(),uname,upass)

            if (reg_s == -1):
                reg = 'Registration Failed, try again later'
            else:
                reg = 'Registration successful, you can close this tab and login.'
        
    return render_template('register.html',reg=reg)

if __name__ == '__main__':
    app.run()
