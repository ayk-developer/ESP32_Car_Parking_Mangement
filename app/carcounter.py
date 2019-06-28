from app.database_handler  import Database

class carcounter():

    def __init__(self):
        self.carlist=[]

    def carin(self,rfid):
        database=Database()
        rfid=database.tagtonumber(rfid)
        self.carlist.append(rfid)

    def carout(self,rfid):
        database=Database()
        rfid=database.tagtonumber(rfid)
        self.carlist.remove(rfid)

    def carcount(self):
        return len(self.carlist)
