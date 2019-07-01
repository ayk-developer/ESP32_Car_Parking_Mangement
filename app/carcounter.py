from app.database_handler  import Database

class carcounter():

    def __init__(self):
        self.carlist=[]

    def carin(self,rfid):
        database=Database()
        self.carlist.append(rfid)

    def carout(self,rfid):
        database=Database()
        self.carlist.remove(rfid)

    def carcount(self):
        return len(self.carlist)

    def cutbill(self):
        #print('shit')
        for car in self.carlist:
            database=Database()
            rfid=database.tagtonumber(car)
            #print(car)
            database.cutbill(rfid)
