import psycopg2
class Database():
    def __init__(self):
        self.conn=psycopg2.connect("dbname='d444nf8njcg92a' user='atwzycuaabdruo' password='91fedb3eee2d763d798890cf015a50f4254b41e84c065cb631eb8d84742c5c40' host='ec2-174-129-41-127.compute-1.amazonaws.com' port='5432'")
        self.cur=self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS parking1(id serial PRIMARY KEY,rfid varchar(20),time abstime NOT NULL DEFAULT CURRENT_TIMESTAMP,inout varchar(5))")
        #self.cur.execute("CREATE TABLE IF NOT EXISTS user(id serial PRIMARY KEY,username varchar(64),email varchar(120),password_hash varchar(128))")
        self.cur.execute("CREATE TABLE IF NOT EXISTS billing(rfid varchar(20) PRIMARY KEY, current_amount INTEGER)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS rfidnumber(rfid varchar(20) PRIMARY KEY, rfidtag varchar(20))")
        #self.cur.execute("CREATE TABLE IF NOT EXISTS accounts(username STRING PRIMARY KEY, password string)")
        #self.conn.commit()
        #self.current_cars=[]

    def tagtonumber(self,tag):
        self.cur.execute('SELECT rfid FROM rfidnumber WHERE rfidtag=%s',(tag,))
        temp=self.cur.fetchall()
        return temp[0][0]

    def logindata(self,username):
        self.cur.execute("SELECT password FROM accounts WHERE username=%s",(username,))
        password=self.cur.fetchall()
        if len(password)==0:
            return "Username is wrong"
        else:
            return password[0][0]



    def carinout(self,rfid_number,inout):
        rfid_number=self.tagtonumber(rfid_number)
        self.cur.execute("INSERT INTO parking1(rfid,inout) VALUES(%s,%s)",[rfid_number,inout])
        self.conn.commit()
        #if inout=="in":
        #    self.current_cars.append(rfid_number)
        #else:
        #    self.current_cars.remove(rfid_number)



    def view(self):
        self.cur.execute("SELECT id,rfid,time,inout FROM parking1")
        row=self.cur.fetchall()
        return row

    def viewbill(self):
        self.cur.execute("SELECT * FROM billing")
        row=self.cur.fetchall()
        return row

    def cutbill(self,rfid):
        self.cur.execute("SELECT current_amount FROM billing WHERE rfid=%s",(rfid,))
        current_amount=self.cur.fetchall()
        #print(type(current_amount[0][0]))
        current_amount=current_amount[0][0]-50
        self.cur.execute("UPDATE billing SET current_amount=%s WHERE rfid=%s",(current_amount,rfid))
        self.conn.commit()

    def addbill(self,rfid,tag,amount):
        #self.cur.execute("IF NOT EXISTS (SELECT current_amount FROM billing WHERE rfid=%s) BEGIN INSERT INTO billing VALUES(%s,0) END",(rfid,rfid))
        self.cur.execute("SELECT current_amount FROM billing WHERE rfid=%s",(rfid,))
        current_amount=self.cur.fetchall()
        if len(current_amount)==0:
            self.cur.execute("INSERT INTO billing VALUES(%s,%s)",(rfid,0))
            self.cur.execute("INSERT INTO rfidnumber VALUES(%s,%s)",(rfid,tag))
            #print('good till here')
        self.cur.execute("SELECT current_amount FROM billing WHERE rfid=%s",(rfid,))
        current_amount=self.cur.fetchall()
        print(current_amount)
        current_amount=current_amount[0][0]+amount
        self.cur.execute("UPDATE billing SET current_amount=%s WHERE rfid=%s",(current_amount,rfid))
        self.conn.commit()

    def search(self,rfid):
        self.cur.execute("SELECT * FROM parking1 WHERE rfid=%s",(rfid,))
        row=self.cur.fetchall()
        return row

    def carcount(self):
        self.cur.execute("SELECT COUNT(*) FROM parking1 Where inout = 'in'")
        incar=self.cur.fetchall()[0][0]
        self.cur.execute("SELECT COUNT(*) FROM parking1 Where inout = 'out'")
        outcar=self.cur.fetchall()[0][0]
        amount=incar-outcar
        return amount


#database.carinout("AA0065","in")
#database.carinout("AC0098","in")
#database.carinout("AB0065","in")
#database.cutbill()

#print(database.view())
#database.addbill("AC0098")

#database.cutbill("AB0065")
#database.addbill("AB0065",25000)
#print(database.viewbill())
