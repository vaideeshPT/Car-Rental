import random
import pandas as pd
import datetime


class CarRental():
    
    """CarRental class to create a rentalshop instance"""

    """Class variables represent the price selection based on number of days and VIP card"""
    PRICE_LESS_THAN_A_WEEK = {"HATCHBACK":30, "SEDAN":50, "SUV":100}
    PRICE_MORE_THAN_A_WEEK = {"HATCHBACK":25, "SEDAN":40, "SUV":90}
    VIP_PRICE = {"HATCHBACK":20, "SEDAN":35, "SUV":80}
  
    def __init__(self):
        """ constructors"""
        self.inventory = pd.read_csv("shopinventory.csv") #read shopinventory csv
        self.customerinfo = pd.read_csv("customerinformation.csv") #read customerinformation csv
        self.bill = 0
    
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
    
    carmodels = ("HATCHBACK", "SEDAN", "SUV") #class variable

    def __init__(self):
        """constructors"""
        self.customer_name = ""
        self.cartype = ""
        self.period = 0
        self.customer_ID = 0   
    
    def __repr__(self):
        return self.customer_name
    
    def requestcar(self, VIP_card):
        """takes a request from the customer asking name, cartype, number of days, VIP status"""

        while True:
            self.customer_name = input('Please enter your name or (type "cancel" to exit): ').upper()
            if self.customer_name.upper() == "CANCEL":
                return None
            else:
                if not self.customer_name.replace(" ", "").isalpha():
                    print("Non alphabet characters are detected. Please try again")
                    print()
                    continue
                    
            a = True       
            while a:
                try:
                    self.period = int(input('Enter the number of days you would like to rent a car or (type 0 to exit): '))
                    if self.period == 0:
                        return None
                except:
                    print("Invalid format. Please try again")
                    print()
                    continue
                else:
                    if self.period > 0:
                        a = False
                        while not a:
                            self.cartype = input('Please enter the car type you want to rent or (type "cancel" to exit): ').upper()
                            if self.cartype.upper() == "CANCEL":
                                return None
                            else:
                                if self.cartype in Customer.carmodels:
                                    return self.customer_name, self.cartype, self.period, VIP_card
                                else:
                                    print("Please enter the correct car model. Please try again")
                                    print()
                                    continue
                    else:
                        print("Negative values are not acceptable. Please try again")
                        print()
                        continue
                    
                    
    def returncar(self):  
        """accepts a unique id from the customer"""

        while True:
            try:
                self.customer_ID = int(input('Please enter your 4-digit customer ID number or (type 0 to exit): '))
                if self.customer_ID == 0:
                    return None
                else:
                    self.customer_ID = str(self.customer_ID)
            except:
                print("Invalid format. Please try again")
                continue
            else:
                if len(self.customer_ID) != 4:
                    print("Not 4 digits. Please try again")
                    continue
                else:
                    return int(self.customer_ID)
                
class VIP(Customer):
    """VIP class to create a vip instance"""

    def __init__(self):
        """constructor"""

        self.VIP_card = "YES"
        Customer.__init__(self)
            
    def requestcar(self, VIP_card):
        """takes a request from the customer asking name, cartype, number of days, VIP status"""
        while True:
            self.customer_name = input('Please enter your name or (type "cancel" to exit): ').upper()
            if self.customer_name.upper() == "CANCEL":
                return None
            else:
                if not self.customer_name.replace(" ", "").isalpha():
                    print("Non alphabet characters are detected. Please try again")
                    print()
                    continue
                    
            a = True       
            while a:
                try:
                    self.period = int(input('Enter the number of days you would like to rent a car or (type 0 to exit): '))
                    if self.period == 0:
                        return None
                except:
                    print("Invalid format. Please try again")
                    print()
                    continue
                else:
                    if self.period > 0:
                        a = False
                        while not a:
                            self.cartype = input('Please enter the car type you want to rent or (type "cancel" to exit): ').upper()
                            if self.cartype.upper() == "CANCEL":
                                return None
                            else:
                                if self.cartype in Customer.carmodels:
                                    return self.customer_name, self.cartype, self.period, VIP_card
                                else:
                                    print("Please enter the correct car model. Please try again")
                                    print()
                                    continue
                    else:
                        print("Negative values are not acceptable. Please try again")
                        print()
                        
        
                
    
   

