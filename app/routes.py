from app import carcounter
from app import app
from app import db
from flask import render_template,request,flash,redirect,url_for
from app.forms import LoginForm,RegistrationForm
from flask_login import current_user, login_user,logout_user,login_required
from app.models import User
from app.database_handler  import Database
from tabulate import tabulate



@app.route('/')
@app.route("/index")
def index():
    carcount=carcounter.carcount()
    print(carcount)
    return render_template("homepage.html",carcount=carcount)

@app.route('/about/')
def about():
    return render_template("about.html")

@app.route('/login/',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('loggined'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
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
    #if (request.form["username"] == "Aung Ye Kyaw") & (request.form["password"] == "11111111"):
        database=Database()
        table = tabulate(database.view(), tablefmt='html')
        return render_template("parkingdata.html",table=table)

@app.route('/billingdata/')
@login_required
def billingdata():
        database=Database()
        table = tabulate(database.viewbill(), tablefmt='html')
        return render_template("parkingdata.html",table=table)

@app.route('/searchdata/',methods=['POST'])
@login_required
def searchdata():
        #a=Database()
    if request.method == 'POST':
        data= (request.form["rfid"])
        database=Database()
        table = tabulate(database.search(data), tablefmt='html')
        return render_template("parkingdata.html",table=table)
        #table = tabulate(request.form["rfid"].search(), tablefmt='html')
        #return render_template("parkingdata.html",table=table)
    return "aaa"

@app.route('/getdata/',methods=['GET','POST'])
def getdata():
    if request.method == 'POST':
        rfid = request.form.get('rfid')
        inout= request.form.get('inout')
        pwd=request.form.get('pwd')
        if pwd == 'lolhaha':

            database=Database()
            database.carinout(rfid,inout)
            if inout == 'in':
                carcounter.carin(rfid)
            elif inout == 'out':
                carcounter.carout(rfid)
            else:
                pass
        else:
            return '''<h1>BUUUUUUUU BUU DESU WA</h1><img src="https://vignette.wikia.nocookie.net/love-live/images/2/27/LLSS_S1Ep1_250.png/revision/latest/scale-to-width-down/800?cb=20160703203036" alt="BUUUUUUUU BUUU DESU WA">'''

    return '''<form method="POST">
                  rfid: <input type="text" name="rfid"><br>
                  inout: <input type="text" name="inout"><br>
                  pwd: <<input type="text" name="pwd"><br>
                  <input type="submit" value="Submit"><br>
              </form>
              '''

@app.route('/addbill/', methods=['GET','POST'])
@login_required
def addbill():
    if request.method == 'POST':
        rfid = request.form.get('rfid')
        amount= request.form.get('amount')
        database=Database()
        database.addbill(rfid,int(amount))
        table = tabulate(database.viewbill(), tablefmt='html')
        return render_template("parkingdata.html",table=table)
    else:
        return render_template('addbill.html')
