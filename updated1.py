
import csv
import sys
import datetime


class Dispense:

    def __init__(self ,patient_name ,drug_name , qty ):
        self.patient_name = patient_name
        self.drug_name = drug_name
        self.qty = qty

    def readdata(self):
        database = []
        f = open("Database", 'rt')
        reader = csv.DictReader(f)
        for row in reader:
            database.append(row)

        f.close()
        return database

    def writedata(self , list):
        f = open("Database", 'wt')
        fieldnames = ('stock_id', 'dist_id','qty' , 'manfac_date' , 'exp_date' , 'drug_id' , 'brand_name', 'unit_price')
        headers = dict((n,n) for n in fieldnames)
        write = csv.DictWriter(f, fieldnames=fieldnames)
        write.writerow(headers)
        for c in list:
            write.writerow(c)
        f.close


    def dispense(self):
        med = Medicine(self.drug_name)
        check = med.isDrugAvailable()
        if check == False :
            print("Drug Not Available Please")


        else:
            #dispense
            #which is just basically upadating the database read into a list and writing it back
            data = self.readdata()
            for row in data:
                if row['brand_name'] == self.drug_name:
                    #update
                    row['qty'] = str(int(row['qty']) - self.qty)
                    self.writedata(data)
                    print("Drug  Dispensed ")
                    print( "Name     %s" %row['brand_name'] )
                    print( "Quantity    %d" % int(row['qty']) )
                    print( "Expiry Date    %s" %row['exp_date'] )
                    print( "Price     %s" %row['unit_price'] )





class Medicine:
    def __init__(self ,name):
        self.name = name
        f = open("Database", 'rt')
        reader = csv.DictReader(f)
        flag  = False
        for row in reader:
            if row['brand_name'] == self.name:
                self.stock_id = row['stock_id']
                self.dist_id = row['dist_id']
                self.qty = row['qty']
                self.manfac_date = row['manfac_date']
                self.exp_date = row['exp_date']
                self.drug_id = row['drug_id']
                self.brand_name  = row['brand_name']
                self.unit_price = row['unit_price']
                flag = True
                break

        if flag == False:
            self.stock_id = 'n/a'
            self.dist_id = 'n/a'
            self.qty = 'n/a'
            self.manfac_date = 'n/a'
            self.exp_date = 'n/a'
            self.drug_id = 'n/a'
            self.brand_name  = 'n/a'
            self.unit_price = 'n/a'

    def isDrugAvailable(self):
        return  False if self.stock_id == 'n/a' else  True





    def  __str__(self):
        return 'Drug name -- ' + str(self.brand_name)  + '\n Quantity -- ' + str(self.qty) + '\nStock id  -- '  + str(self.stock_id) +'\nUnit price -- ' + str(self.unit_price) +"\nDistributer id --   " + str(self.dist_id) + " \nExpiry Date ->  "  + str(self.exp_date) +  "\nManufacturing Date ->    " + str(self.manfac_date)







class Stock :


    def __init__(self, stockid, distid, qty, manudate , exdate  ,drugid , brandname , unitprice   ):
        self.stock_id = stockid
        self.dist_id = distid
        self.qty= qty
        self.manfac_date= manudate
        self.exp_date = exdate
        self.drug_id  = drugid
        self.brand_name = brandname
        self.unit_price = unitprice


    def __str__(self):
        return 'stock id--' + str(self.stock_id)  + 'distributor--'+ str(self.dist_id) + 'quantity--' + str(self.qty)+'manufacturing date--'+str(self.manfac_date)+'expiring date--'+str(self.exp_date)

    #read whole database in memory not the best implementation possible
    def readdata(self):
        database = []
        f = open("Database", 'rt')
        reader = csv.DictReader(f)
        for row in reader:
            database.append(row)

        f.close()
        return database




    def increaseStock(self):

        flag  =  False
        #read whole database into database
        database = self.readdata()

        for row in database:
            if row['brand_name'] == self.brand_name:
                row['qty'] =  str(int(row['qty']) +int(self.qty))
                flag = True
                #write everything back into the database
                f = open("Database", 'wt')
                fieldnames = ('stock_id', 'dist_id','qty' , 'manfac_date' , 'exp_date' , 'drug_id' , 'brand_name', 'unit_price')
                headers = dict((n,n) for n in fieldnames)
                write = csv.DictWriter(f, fieldnames=fieldnames)
                write.writerow(headers)
                for c in database:
                    write.writerow(c)
                f.close
                break
        if flag == False:
            #if not found then it must be a new drug
            f = open("Database", 'at')
            fieldnames = ('stock_id', 'dist_id','qty' , 'manfac_date', 'exp_date' , 'drug_id' , 'brand_name', 'unit_price')
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            row = dict( stock_id= self.stock_id ,dist_id=self.dist_id ,qty=self.qty , manfac_date=self.manfac_date ,exp_date=self.exp_date , drug_id=self.drug_id , brand_name=self.brand_name , unit_price=self.unit_price )
            writer.writerow(row)
            f.close()

    def viewAddedStock(self):
        f = open("Database", 'rt')
        reader = csv.DictReader(f)
        for row in reader:
            if int(row['qty']) >= int(self.qty):
                print(row)



        f.close()




#Main Program Starts Here

while True:
    print("Enter                           To")
    print("D                           To Dispense             ")
    print("A                           Add Item(s) To The Stock")
    print("S                           View Inventory Statistics")
    print("R                           Remove Item(s)  From the Stock")
    print("Q                           To quit the program ")

    inp  = input("Enter Your choice ->  ")

    if inp.upper() == 'D':
        name = input("Enter Patient's Name  -> ")
        drug = input("Enter Drug Name  ->")
        qty  = input("Enter Drug Quantity  ->  ")
        dispense = Dispense(name ,drug ,qty)


    elif inp.upper() == 'A':
        #('stock_id', 'dist_id','qty' , 'manfac_date', 'exp_date' , 'drug_id' , 'brand_name', 'unit_price')

        stockid  = input("Enter Stock id  ->  ")
        drugname = input("Enter Drug Name -> ")
        distid = input("Enter Distributer id  -> ")
        qty = input("Enter Drug Quantity ->  ")
        manfac = input("Enter Manufacturing Date(YY-MM-DD) -> ")
        expdate = input("Enter Expiry Date(YY-MM-DD) ->")
        drug_id = input("Enter Drug id  -> ")
        price = input("Enter Price -> ")
        stock = Stock(stockid , distid , qty ,manfac , expdate , drug_id , drugname , price)
        stock.increaseStock()
        stock.viewAddedStock()

    elif inp.upper() == 'S':
        database = []
        f = open("Database", 'rt')
        reader = csv.DictReader(f)
        total = 0
        for row in reader:
            database.append(row)
            total +=1

        f.close()

        print("Total Number of Items In Inventory  ---> %d " %total )
        #'stock_id', 'dist_id','qty' , 'manfac_date' , 'exp_date' , 'drug_id' , 'brand_name', 'unit_price'

        print("\n\n                              List  of Drugs in the inventory ")
        print("***********************************************************************************************")
        print(" Drug Name       Stock id   Distributer id   Quantity  Manufacturing Date  Expiry Date  Drug id   Price   \n")
        for c in database:
            print("%15s      %5s       %5s        %5%                %10s        %10s       %5s       %5s   " ,c['brand_name'] , c['stock_id'] , c['dist_id'],  c['qty']
            ,c['manfac_date']  , c['exp_date'] , c['drug_id'] , c['unit_price'])


    elif inp.upper() == 'R':
        drug = input("Enter Name of  Drug to Remove  -->  ")
        database = []
        f = open("Database", 'rt')
        reader = csv.DictReader(f)
        for row in reader:
            database.append(row)


        f.close()
        i = -1
        flag = False
        for row in database:
            i +=1
            if row['brand_name'] == drug:
                    #update
                flag = True
                database.pop(i)
                f = open("Database", 'wt')
                fieldnames = ('stock_id', 'dist_id','qty' , 'manfac_date' , 'exp_date' , 'drug_id' , 'brand_name', 'unit_price')
                headers = dict((n,n) for n in fieldnames)
                write = csv.DictWriter(f, fieldnames=fieldnames)
                write.writerow(headers)
                for c in list:
                        write.writerow(c)
                f.close

        if(flag == False):
            print("Drug Not Available in the Inventory")




    elif inp.upper == 'Q':
        print("Goodbye Have A nice Day ")
        exit()



    else:
        print("Unknown Command, Please Try Again ")



