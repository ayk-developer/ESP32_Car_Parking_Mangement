class carcounter():

    def __init__(self):
        self.carlist=[]

    def carin(self,rfid):
        self.carlist.append(rfid)

    def carout(self,rfid):
        self.carlist.remove(rfid)

    def carcount(self):
        return len(self.carlist)
