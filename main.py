import carshop



def main():
                    
    rentalshop = CarRental()
    customer = Customer()
    
    while True:
        print("""
        These are the services offered by us
        1. Available Stock and Prices
        2. Renting a car 
        3. Return the car
        4. Exit
        """)
        
        try:
            option = int(input("Please select the service you are interested in: "))
            print()
        except ValueError:
            print("Invalid format. Try again")
            continue
        
        if option == 1:
            rentalshop.display_stock_and_prices()
            continue
        
        elif option == 2:
            
            VIP_card = check_VIP_status()
            
            if VIP_card == "CANCEL":
                break
            elif VIP_card != "YES":
                rentalshop.rentcar(customer.requestcar(VIP_card))
            else:
                rentalshop.rentcar(vipcustomer.requestcar(VIP_card))
            break
           
        elif option == 3:
            rentalshop.getthebill(customer.returncar())
            break
          
        elif option == 4:
            break
                 
        else:
            print("Invalid input. Please enter number between 1-4 ")
            continue
    print()
    print("Thank you for using our car rental service. Hope to see you again.")
        


if __name__=="__main__":
    print("Welcome to Python Car Rental Shop", end = "\n")
    main()