import random
import sqlite3
import pandas as pd
import datetime

CARMODELS = ("HATCHBACK", "SEDAN", "SUV")
PRICE_LESS_THAN_A_WEEK = {"HATCHBACK":30, "SEDAN":50, "SUV":100}
PRICE_MORE_THAN_A_WEEK = {"HATCHBACK":25, "SEDAN":40, "SUV":90}
VIP_PRICE = {"HATCHBACK":20, "SEDAN":35, "SUV":80}

def create_db():
    try:
        conn = sqlite3.connect('shop.db')
    except:
        print("Database is not created")

create_db()


class CarRental():
  
    def __init__(self):

        self.inventory = None
        self.customerinfo = None
        self.bill = 0

    def get_inventory(self):
        pass

    def update_inventory(self):
        pass

    def get_customerinfo(self):
        pass

    def update_customerinfo(self):
        pass
    
    def display_stock_and_prices(self):
        pass

    def generateID(self):
        pass

    def getcar(self):
        pass

    def getbill(self):
        pass



    def display_stock_and_prices(self):
        """ displays currently available car models and prices"""
        
        quantity = tuple(self.inventory["Quantity"])
        data = [[quantity[0],"£30","£25","£20"], [quantity[1],"£50","£40","£35"], [quantity[2],"£100","£90","£80"]]
        df_stock_and_prices = pd.DataFrame(data, columns = ["Available cars", "Price 1", "Price 2", "Price 3"],
                                        index = ["HATCHBACK", "SEDAN", "SUV"])
        print("*****************************************************************")
        print(df_stock_and_prices)
        print()
        print("Price 1 ---> price for renting a car for less than a week", end="\n")
        print("Price 2 ---> price for renting a car for more than a week", end="\n")
        print("Price 3 ---> VIP Price", end="\n")
        print("*****************************************************************")
        
        
    @classmethod
    def week(cls, period, VIP_card):
        """returns a class variable based on period and VIP_card"""
        
        if VIP_card == "NO":
            if period < 7:
                return cls.PRICE_LESS_THAN_A_WEEK
            else:
                return cls.PRICE_MORE_THAN_A_WEEK
        else:
            return cls.VIP_PRICE
     
        
    @staticmethod
    def generateID():
        """generates four digit unique ID"""
        
        ID_tuple = tuple(pd.read_csv("customerinformation.csv")["Customer_ID"])
        customer_ID = 0
        
        while True:
            number = random.randint(1000,9999)
            if number in ID_tuple:
                continue
            else:
                customer_ID = number
                break
        return customer_ID
    
    
    def rentcar(self, arg):
        """rents a car to a customer"""

        if arg is None:
            return None
        else:
            customer_name, cartype, period, VIP_card = arg
            check_quantity = self.inventory.loc[(self.inventory["Cartype"] == cartype)]["Quantity"] #check inventory
            check_quantity_int = int(check_quantity) #number of cars
        
            if check_quantity_int > 0:
                start_date = str(datetime.date.today()) #beginning of rent duration
                end_date = str(datetime.date.today() + datetime.timedelta(days = period)) #final date
                rent_time = datetime.datetime.now().strftime("%H:%M") #rented a car on what time
                status = "Live"
                car_price = CarRental.week(period, VIP_card)[cartype]
                total_payment = period*CarRental.week(period, VIP_card)[cartype]
                customer_ID = self.generateID()
            
                self.inventory.loc[self.inventory["Cartype"] == cartype, "Quantity"] = check_quantity_int - 1
                self.inventory.to_csv("shopinventory.csv", index = False) #update inventory after renting a car (-1)
                
                # df write the informations in the csv
                df = pd.DataFrame([customer_ID, customer_name, cartype, car_price, rent_time, start_date,
                                   end_date, period, total_payment, VIP_card, status]).T
                with open("customerinformation.csv", 'a') as file:
                    df.to_csv(file, header = False, index = False)
                    
                print()        
                print(f"Your customer ID number is {customer_ID}. Please save your customer ID safely.")
                print(f"You have rented a {cartype} car for {period} day(s) on {start_date}. The car has to be returned on {end_date}.")
                print(f"You will charged with the amount of £{total_payment}.")
                print()
                print("The current stock is: ", end="\n")
                self.display_stock_and_prices()
                
                print("We hope that you enjoyed our service.")
                
            
            else:
                print(f"Sorry, we do not have a stock of {cartype} model in our shop.")
                
                       
 
    def getthebill(self, arg):
        """returns a bill to the customer"""

        if arg is None:
            return None
        else:
            customer_ID = arg
            ID_column = tuple(self.customerinfo.Customer_ID)

            for index, customer_Id in enumerate(ID_column): #check for customer_ID in customerinformation.csv
                if customer_Id == customer_ID: #if id is in the csv
                    row = list(self.customerinfo.iloc[index])
                    if row[-1] == "Live":
                        status = "Returned" # change status to Returned
                        row = list(self.customerinfo.iloc[index])
                        bill = row[:-1]
                        cartype = bill[2]
            
                        self.customerinfo.loc[self.customerinfo["Customer_ID"]==customer_Id, "Status"] = status
                        self.customerinfo.to_csv("customerinformation.csv", index=False)# update customerinformation csv file
                        update_quantity = self.inventory.loc[(self.inventory["Cartype"] == cartype)]["Quantity"]
                        update_quantity_int = int(update_quantity)
                        self.inventory.loc[self.inventory["Cartype"] == cartype, "Quantity"] = update_quantity_int + 1
                        self.inventory.to_csv("shopinventory.csv", index=False) #update the stock (+1)
                        
                        self.bill = pd.DataFrame(bill, columns = ["Your bill"],index = ["Customer ID", "Name", "Car model", "Car rate (£)", "Time", "Start date", "End date", "Duration", "Total Payment (£)", "VIP card"])  
                        print(self.bill)
                        return self.bill

                    else:
                        print("You have already returned the car to us.")
                        return None
            else:
                print("Your customer ID is not in our system. Please check again.")
                
            
            
            
class Customer(CarRental):
    """Customer class to create a customer instance"""

    def __init__(self):
        
        self.name = ""
        self.carmodel = ""
        self.days = 0
        self.ID = 0

    def requestname(self):

        while True:
            try:
                self.name = input('Please enter your name or (type "cancel" to exit): ').upper()
                if self.name == 'CANCEL':
                    return None
                else:
                    if not self.name(" ","").isalpha():
                        print("Non alphabet characters are detected. Please  try again")
                    else:
                        return self.name
            except:
                print("Non valid characters")

    def requestcarmodel(self):

        while True:
            try:
                self.carmodel = input('Please enter the car model or (type "cancel" to exit): ').upper()
                if self.carmodel == 'CANCEL':
                    return None
                else:
                    if self.carmodel in CARMODELS:
                        return self.cardmodel
                    else:
                        print("Please enter the correct model.")
                        continue
            except:
                print("Non valid characters")


    def requestdays(self):

        while True:
            try:
                self.days = int(input('Please enter how many days or (type 0 to exit): '))
                if self.days < 0:
                    print("No negative value is acceptable.")
                else:
                    return self.days
            except:
                print("Non char")

    def requestcar(self):
        name = self.requestname()
        carmodel = self.requestcarmodel()
        days = self.requestdays()

        return name, carmodel, days

    def returncar(self):  

        while True:
            try:
                self.ID = int(input('Please enter your 4-digit customer ID number or (type 0 to exit): '))
                if self.ID == 0:
                    return None
                else:
                    self.ID = str(self.customer_ID)
            except:
                print("Invalid format. Please try again")
                continue
            else:
                if len(self.customer_ID) != 4:
                    print("Not 4 digits. Please try again")
                    continue
                else:
                    return int(self.customer_ID)