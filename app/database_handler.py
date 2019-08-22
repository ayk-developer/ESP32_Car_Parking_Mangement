import psycopg2
from psycopg2.extensions import AsIs
from psycopg2 import sql
from datetime import datetime
class Database():
    def __init__(self,parking):
        self.parking=parking
        self.conn=psycopg2.connect("dbname='d444nf8njcg92a' user='atwzycuaabdruo' password='91fedb3eee2d763d798890cf015a50f4254b41e84c065cb631eb8d84742c5c40' host='ec2-174-129-41-127.compute-1.amazonaws.com' port='5432'")
        self.cur=self.conn.cursor()

        self.cur.execute("CREATE TABLE IF NOT EXISTS {} (id serial PRIMARY KEY,rfid varchar(20),time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,inout varchar(5))".format(self.parking))
        #self.cur.execute("CREATE TABLE IF NOT EXISTS user(id serial PRIMARY KEY,username varchar(64),email varchar(120),password_hash varchar(128))")
        self.cur.execute("CREATE TABLE IF NOT EXISTS billing(rfid varchar(20) PRIMARY KEY, current_amount INTEGER)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS rfidnumber(rfid varchar(20) PRIMARY KEY, rfidtag varchar(20))")
        #self.cur.execute("CREATE TABLE IF NOT EXISTS accounts(username STRING PRIMARY KEY, password string)")
        self.conn.commit()
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
        self.cur.execute("INSERT INTO {}(rfid,inout) VALUES(%s,%s)".format(self.parking),[rfid_number,inout])
        self.conn.commit()
        #if inout=="in":
        #    self.current_cars.append(rfid_number)
        #else:
        #    self.current_cars.remove(rfid_number)



    def viewadmin(self):
        a=parkinglist()
        temp_dict={}
        for i in a:
            self.cur.execute("SELECT id,rfid,time,inout FROM {}".format(i))
            row=self.cur.fetchall()
            temp_dict.update({i:row})
        return temp_dict
        

    def view(self,rfid):
        a=parkinglist()
        temp_dict={}
        for i in a:
            self.cur.execute("SELECT time,inout FROM {} where rfid =%s".format(i),(rfid,))
            row=self.cur.fetchall()
            temp_dict.update({i:row})
        return temp_dict

    def viewbill(self,rfid):
        self.cur.execute("SELECT * FROM billing where rfid=%s",(rfid,))
        row=self.cur.fetchall()
        return row

    def viwebilladmin(self):
        self.cur.execute("SELECT * FROM billing")
        row=self.cur.fetchall()
        return row

    def cutbill(self,rfid):
        self.cur.execute("select last_value(time) over() from {} where inout='out' limit 1".format(self.parking))
        outtime=self.cur.fetchall()[0][0]
        self.cur.execute("select last_value(time) over() from {} where inout='in' limit 1".format(self.parking))
        intime=self.cur.fetchall()[0][0]
        print(outtime)
        print(intime)
        dur=datetime.strptime(outtime,'%Y-%m-%d %H:%M:%S+%f')-datetime.strptime(intime,'%Y-%m-%d %H:%M:%S+%f')
        cost=int(dur.seconds*0.083)
        print(cost)
        rfid=self.tagtonumber(rfid)
        self.cur.execute("SELECT current_amount FROM billing WHERE rfid=%s",(rfid,))
        current_amount=self.cur.fetchall()
        print(current_amount[0][0])
        current_amount=current_amount[0][0]-cost
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
        self.cur.execute("SELECT * FROM {} WHERE rfid=%s".format(self.parking),(rfid,))
        row=self.cur.fetchall()
        return row

    def carcount(self):
        self.cur.execute("SELECT COUNT(*) FROM {} Where inout = 'in'".format(self.parking))
        incar=self.cur.fetchall()[0][0]
        self.cur.execute("SELECT COUNT(*) FROM {} Where inout = 'out'".format(self.parking))
        outcar=self.cur.fetchall()[0][0]
        amount=incar-outcar
        return amount


def parkinglist():
    conn=psycopg2.connect("dbname='d444nf8njcg92a' user='atwzycuaabdruo' password='91fedb3eee2d763d798890cf015a50f4254b41e84c065cb631eb8d84742c5c40' host='ec2-174-129-41-127.compute-1.amazonaws.com' port='5432'")
    cur=conn.cursor()

    cur.execute("SELECT tablename FROM pg_catalog.pg_tables where schemaname='public'")

    a=[item[0] for item in cur.fetchall()]

    a.remove('billing')
    a.remove('rfidnumber')
    a.remove('user1')
    return a

def occupied():
    conn=psycopg2.connect("dbname='d444nf8njcg92a' user='atwzycuaabdruo' password='91fedb3eee2d763d798890cf015a50f4254b41e84c065cb631eb8d84742c5c40' host='ec2-174-129-41-127.compute-1.amazonaws.com' port='5432'")
    cur=conn.cursor()
    a=parkinglist()
    temp_dict={}
    for i in a:
        cur.execute("SELECT COUNT(*) FROM {} Where inout = 'in'".format(i))
        incar=cur.fetchall()[0][0]
        cur.execute("SELECT COUNT(*) FROM {} Where inout = 'out'".format(i))
        outcar=cur.fetchall()[0][0]
        amount=incar-outcar
        temp_dict.update({i:amount})
    return temp_dict

        



#database=Database('lol')
#database.carinout("AA0065","in")
#database.carinout("AC0098","in")
#database.carinout("AB0065","in")
#database.cutbill()

#print(database.view())
#database.addbill("AC0098")

#database.cutbill("AB0065")
#database.addbill("AB0065",25000)
#print(database.viewbill())
