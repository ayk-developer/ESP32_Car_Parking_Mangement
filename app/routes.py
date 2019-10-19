#from app import carcounter
from app import app
from app import db
from flask import render_template,request,flash,redirect,url_for,Response,jsonify
from app.forms import LoginForm,RegistrationForm
from flask_login import current_user, login_user,logout_user,login_required
from app.models import User
from app.database_handler  import Database,occupied
from tabulate import tabulate



@app.route('/')
@app.route("/index")
def index():
    carcount=occupied()
    return render_template("homepage.html",carcount=carcount)

@app.route('/about/')
def about():
    return render_template("about.html")

@app.route('/login/',methods=['GET','POST'])
def login():
    status=0
    if current_user.is_authenticated:
        return redirect(url_for('loggined'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('<li>Invalid username or password</li>')
            status=1
            print("flashed")
            #return redirect(url_for('login'))
            return render_template('login.html', form=form,status=status)
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('loggined'))
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/loggined')
def loggined():
    return render_template('loggined.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/parkingdata/')
@login_required
def parkingdata():
    table=[]
    parking_names=[]
    database=Database('parking1')
    if current_user.username=='Admin':
        temp_dict=database.viewadmin()
        for i in temp_dict: 
            table.append(tabulate(temp_dict[i], tablefmt='html'))
            parking_names.append(i)
        return render_template("parkingdata.html",table=zip(parking_names,table))
    else:
        temp_dict=database.view(current_user.username)
        for i in temp_dict: 
            table.append(tabulate(temp_dict[i], tablefmt='html'))
            parking_names.append(i)
        return render_template("parkingdata.html",table=zip(parking_names,table))

@app.route('/map/')
def map():
    return render_template("map.html")

@app.route('/billingdata/')
@login_required
def billingdata():
    database=Database('parking1')
    if current_user.username=='Admin':
        table = tabulate(database.viwebilladmin(), tablefmt='html')
        return render_template("billingdata.html",table=table)
    else:
        table = tabulate(database.viewbill(current_user.username), tablefmt='html')
        return render_template("billingdata.html",table=table)

@app.route("/searchbill/",methods=["POST"])
@login_required
def searchbill():
    if current_user.username=='Admin':
        if request.method== 'POST':

            database=Database('parking1')
            data= (request.form["rfid"])

            table = tabulate(database.viewbill(data), tablefmt='html')
            return render_template("billingdata.html",table=table)




@app.route('/searchdata/',methods=['POST'])
@login_required
def searchdata():
    if current_user.username=='Admin':
        #a=Database('parking1')
        if request.method == 'POST':
            table=[]
            parking_names=[]
            data= (request.form["rfid"])
            database=Database('parking1')
            temp_dict=database.view(data)
            for i in temp_dict: 
                table.append(tabulate(temp_dict[i], tablefmt='html'))
                parking_names.append(i)
            return render_template("parkingdata.html",table=zip(parking_names,table))
            #table = tabulate(request.form["rfid"].search(), tablefmt='html')
            #return render_template("parkingdata.html",table=table)
        return "aaa"
    else:
        return "<h1>You Dont Have Permission to access Here</h1>"
    

@app.route('/getdata/',methods=['GET','POST'])
def getdata():
    if request.method == 'POST':
        rfid = request.form.get('rfid')
        inout= request.form.get('inout')
        pwd=request.form.get('pwd')
        a=request.form.get('parking')
        if pwd == 'lolhaha':

            database=Database(a)
            database.carinout(rfid,inout)
            if inout == 'out':
                print('got to out')
                database.cutbill(rfid)
            #database.viewbill(rfid)
            b=database.viewbill(rfid)
            Car_Number=b[0][0]
            Balance=b[0][1]
            print(Car_Number,Balance)
            return jsonify(car_number=Car_Number,balance=Balance)
            '''
            if inout == 'in':
                carcounter.carin(rfid)
            elif inout == 'out':
                carcounter.carout(rfid)
            else:
                pass
            '''
        else:
            return '''<h1>BUUUUUUUU BUU DESU WA</h1><img src="https://vignette.wikia.nocookie.net/love-live/images/2/27/LLSS_S1Ep1_250.png/revision/latest/scale-to-width-down/800?cb=20160703203036" alt="BUUUUUUUU BUUU DESU WA">'''

    return '''<form method="POST">
                  rfid: <input type="text" name="rfid"><br>
                  inout: <input type="text" name="inout"><br>
                  pwd: <input type="text" name="pwd"><br>
                  parking : <input type="text" name="parking"><br>
                  <input type="submit" value="Submit"><br>
              </form>
              '''

@app.route('/addbill/', methods=['GET','POST'])
@login_required
def addbill():
    if current_user.username=='Admin':
        if request.method == 'POST':
            rfid = request.form.get('rfid')
            amount= request.form.get('amount')
            tag=request.form.get('tag')
            database=Database('parking1')
            database.addbill(rfid,tag,int(amount))
            table = tabulate(database.viwebilladmin(), tablefmt='html')
            return render_template("parkingdata.html",table=table)
        else:
            return render_template('addbill.html')
    else:
        return "<h1>You Dont Have Permission to access Here</h1>"
