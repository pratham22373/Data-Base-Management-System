import datetime
import time
import mysql.connector

# Establishing connection to the MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sachin1234",
    database="GIFTSTORE"
)

# Function to view orders
def view_orders(customer_id):
    cursor = db_connection.cursor()
    query = "SELECT o.OrderID, p.ProductName, o.Quantity, o.Status_ FROM Orders o JOIN Product p ON o.ProductID = p.ProductID WHERE o.CustomerID = %s"
    cursor.execute(query, (customer_id,))
    orders = cursor.fetchall()
    cursor.close()

    if orders:
        print("Your Orders:")
        for order in orders:
            order_id, product_name, quantity, status = order
            print(f"Order ID: {order_id}, Product Name: {product_name}, Quantity: {quantity}, Status: {status}")
    else:
        print("You have no orders.")

# Function to view all products
def view_products():
    db_connection.commit()
    cursor = db_connection.cursor()
    query = "SELECT ProductID, ProductName, ProductType, ProductPrice, Stock, RefundableStatus, ProductDescription, Stars FROM Product"
    cursor.execute(query)
    products = cursor.fetchall()
    cursor.close()

    print("All Products:")
    for product in products:
        product_id, product_name, product_type, product_price, stock, refundable_status, product_description, stars = product
        print(f"ID: {product_id}, Name: {product_name}, Type: {product_type}, Price: ${product_price:.2f}, Stock: {stock}, RefundableStatus: {'Yes' if refundable_status else 'No'}, Description: {product_description}, Stars: {stars}")


# Function to filter products by name
def filter_by_name():
    name = input("Enter the product name: ").lower()
    cursor = db_connection.cursor()
    query = "SELECT ProductID, ProductName, ProductType, ProductPrice, Stock, RefundableStatus, ProductDescription, Stars FROM Product WHERE LOWER(ProductName) LIKE %s"
    cursor.execute(query, ('%' + name + '%',))
    filtered_products = cursor.fetchall()
    cursor.close()

    if filtered_products:
        print("Filtered Products:")
        for product in filtered_products:
            print(product)
    else:
        print("No such product.")

# Function to filter products by rating
def filter_by_rating():
    rating = float(input("Enter the minimum rating (1-5): "))
    cursor = db_connection.cursor()
    query = "SELECT ProductID, ProductName, ProductType, ProductPrice, Stock, RefundableStatus, ProductDescription, Stars FROM Product WHERE Stars >= %s"
    cursor.execute(query, (rating,))
    filtered_products = cursor.fetchall()
    cursor.close()

    if filtered_products:
        print("Filtered Products:")
        for product in filtered_products:
            print(product)
    else:
        print("No such product.")

# Function to filter products by price
def filter_by_price():
    price = float(input("Enter the minimum price in $: "))
    cursor = db_connection.cursor()
    query = "SELECT ProductID, ProductName, ProductType, ProductPrice, Stock, RefundableStatus, ProductDescription, Stars FROM Product WHERE ProductPrice >= %s"
    cursor.execute(query, (price,))
    filtered_products = cursor.fetchall()
    cursor.close()

    if filtered_products:
        print("Filtered Products:")
        for product in filtered_products:
            print(product)
    else:
        print("No such product.")


# Function to filter products by refundable status
def filter_by_refundable():
    cursor = db_connection.cursor()
    query = "SELECT ProductID, ProductName, ProductType, ProductPrice, Stock, RefundableStatus, ProductDescription, Stars FROM Product WHERE RefundableStatus = 1"
    cursor.execute(query)
    filtered_products = cursor.fetchall()
    cursor.close()

    print("Filtered Products:")
    for product in filtered_products:
        print(product)

# Main menu
def main_menu(dbconnection):
    while True:
        print("\nMain Menu:")
        print("1. Enter as Customer")
        print("2. Enter as Vendor")
        print("3. Enter as Admin")  # Option to login as Admin
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            customer_menu(dbconnection)
        elif choice == '2':
            vendor_menu(db_connection)
        elif choice == '3':
            admin_login()  # Call the admin login function
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")


# Customer menu
def customer_menu(dbconnection):
    while True:
        print("\nCustomer Menu:")
        print("1. Login")
        print("2. Signup")
        print("3. Back to main menu")
        choice = input("Enter your choice: ")
        if choice == '1':
            customer_login()
        elif choice == '2':
            customer_signup(dbconnection)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please enter a valid option.")

def add_to_cart(customer_id):
    try:
        cursor = db_connection.cursor()  # Define cursor here

        # Begin transaction
        db_connection.start_transaction()

        cursor.execute("SELECT * FROM customer WHERE customer_id = %s", (customer_id,))
        customer = cursor.fetchone()

        if not customer:
            # If customer does not exist, insert the customer into the customer table
            insert_customer_query = "INSERT INTO customer (customer_id, NumberOfOrdersPlaced) VALUES (%s, %s)"
            cursor.execute(insert_customer_query, (customer_id, 0))  # Defaulting NumberOfOrdersPlaced to 0

        product_id = int(input("Enter the Product ID: "))
        quantity = int(input("Enter the Quantity: "))

        # Check if the product exists
        check_product_query = "SELECT * FROM Product WHERE ProductID = %s"
        cursor.execute(check_product_query, (product_id,))
        product = cursor.fetchone()

        if product:
            # Check if the product is already in the cart
            check_cart_query = "SELECT * FROM CART WHERE CustomerID = %s AND ProductID = %s"
            cursor.execute(check_cart_query, (customer_id, product_id))
            existing_cart_item = cursor.fetchone()

            if existing_cart_item:
                # If product is already in cart, update its quantity
                update_quantity_query = "UPDATE CART SET quantity = quantity + %s WHERE CustomerID = %s AND ProductID = %s"
                cursor.execute(update_quantity_query, (quantity, customer_id, product_id))
            else:
                # Check if there is sufficient stock
                stock = product[4]  # Index 4 corresponds to Stock in the product tuple
                if quantity <= stock:
                    # Insert into cart table
                    insert_query = "INSERT INTO CART (CustomerID, ProductID, quantity) VALUES (%s, %s, %s)"
                    cursor.execute(insert_query, (customer_id, product_id, quantity))
                else:
                    print("Not enough stock available.")
        else:
            print("No such product.")

        # Commit the transaction
        db_connection.commit()
        print("Transaction committed successfully!")
    except ValueError:
        print("Invalid input for Product ID or Quantity.")
        db_connection.rollback()  # Rollback the transaction on error
    except mysql.connector.Error as err:
        print("Error:", err)
        db_connection.rollback()  # Rollback the transaction on error
    finally:
        cursor.close()  # Close cursor in the finally block



# Function to view cart
def view_cart(customer_id):
    cursor = db_connection.cursor()
    query = "SELECT c.ProductID, p.ProductName, p.ProductPrice, c.quantity FROM CART c JOIN Product p ON c.ProductID = p.ProductID WHERE CustomerID = %s"
    cursor.execute(query, (customer_id,))
    cart_items = cursor.fetchall()
    cursor.close()

    if cart_items:
        total_cost = 0
        print("Your Cart:")
        for item in cart_items:
            product_id, product_name, product_price, quantity = item
            total_cost += product_price * quantity
            print(f"Product ID: {product_id}, Name: {product_name}, Price: {product_price}, Quantity: {quantity}")
        print(f"Total Cost: ${total_cost}")
    else:
        print("Your cart is empty.")

# Customer login function
# Function to remove products from cart
def remove_from_cart(customer_id):
    try:
        product_id = int(input("Enter the Product ID to remove: "))
        quantity_to_remove = int(input("Enter the quantity to remove: "))
        cursor = db_connection.cursor()

        # Begin transaction
        db_connection.start_transaction()

        # Check if the product exists in the cart
        query = "SELECT Quantity FROM CART WHERE CustomerID = %s AND ProductID = %s"
        cursor.execute(query, (customer_id, product_id))
        cart_item = cursor.fetchone()

        if cart_item:
            current_quantity = cart_item[0]
            if quantity_to_remove > current_quantity:
                print("Error: Quantity to remove exceeds the quantity in the cart.")
            elif quantity_to_remove == current_quantity:
                # Remove the product completely from the cart
                delete_query = "DELETE FROM CART WHERE CustomerID = %s AND ProductID = %s"
                cursor.execute(delete_query, (customer_id, product_id))
                print("Product removed from cart successfully!")
            else:
                # Update the quantity of the product in the cart
                new_quantity = current_quantity - quantity_to_remove
                update_query = "UPDATE CART SET Quantity = %s WHERE CustomerID = %s AND ProductID = %s"
                cursor.execute(update_query, (new_quantity, customer_id, product_id))
                print("Quantity updated in the cart successfully!")
        else:
            print("Product not found in your cart.")

        # Commit the transaction
        db_connection.commit()
        print("Transaction committed successfully!")
    except ValueError:
        print("Invalid input for Product ID or Quantity.")
        db_connection.rollback()  # Rollback the transaction on error
    except mysql.connector.Error as err:
        print("Error:", err)
        db_connection.rollback()  # Rollback the transaction on error
    finally:
        cursor.close()

def manage_wallet(customer_id):
    while True:
        print("\nWallet Management:")
        print("1. Add cash to wallet")
        print("2. View wallet balance")
        print("3. Back to Customer Menu")
        choice = input("Enter your choice: ")
        if choice == '1':
            add_money_to_wallet(customer_id)
        elif choice == '2':
            view_wallet(customer_id)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please enter a valid option.")

# Function to view customer profile
def view_profile(customer_id):
    cursor = db_connection.cursor()
    query = "SELECT * FROM person WHERE person_id = %s"
    cursor.execute(query, (customer_id,))
    customer_profile = cursor.fetchone()
    cursor.close()

    if customer_profile:
        print("Customer Profile:")
        print(f"ID: {customer_profile[0]}")
        print(f"First Name: {customer_profile[1]}")
        print(f"Middle Name: {customer_profile[2]}" if customer_profile[2] else "Middle Name: N/A")
        print(f"Last Name: {customer_profile[3]}")
        print(f"Phone Number: {customer_profile[4]}")
        print(f"Email: {customer_profile[5]}")
        print(f"Street ID: {customer_profile[6]}")
        print(f"City: {customer_profile[7]}")
        print(f"Landmark: {customer_profile[8]}")
        print(f"State: {customer_profile[9]}")
        print(f"Pincode: {customer_profile[10]}")
        print(f"Date of Birth: {customer_profile[11]}")
        
    else:
        print("Customer profile not found.")



# Customer login function
def customer_login():
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    try:
        cursor = db_connection.cursor()

        # Check if the user is locked out
        cursor.execute("SELECT locked_until FROM LockedUsers WHERE email = %s", (email,))
        locked_until_time = cursor.fetchone()
        if locked_until_time and locked_until_time[0] > datetime.datetime.now():
            print("This email is banned. Try again after some time.")
            return

        # Verify login credentials
        cursor.execute("SELECT * FROM person WHERE email = %s AND password_ = %s", (email, password))
        customer = cursor.fetchone()

        if customer:
            print("Login successful as Customer!")
            # Reset login attempts
            cursor.execute("UPDATE LoginAttempts SET attempts = 0 WHERE email = %s", (email,))
            db_connection.commit()

            # Proceed with the rest of the login process
            while True:
                print("\nCustomer Menu:")
                print("1. View Products")
                print("2. Filter Search")
                print("3. Add Product to Cart")
                print("4. Remove Product from Cart")
                print("5. View Cart")
                print("6. Buy from Cart")
                print("7. View Orders")
                print("8. Manage Wallet")
                print("9. View Profile")  # New option to view profile
                print("10. Logout")
                choice = input("Enter your choice: ")
                if choice == '1':
                    view_products()
                elif choice == '2':
                    filter_menu()
                elif choice == '3':
                    add_to_cart(customer[0])  # Pass CustomerID to add_to_cart function
                elif choice == '4':
                    remove_from_cart(customer[0])  # Pass CustomerID to remove_from_cart function
                elif choice == '5':
                    view_cart(customer[0])  # Pass CustomerID to view_cart function
                elif choice == '6':
                    buy_from_cart(customer[0] , email)  # Pass CustomerID to buy_from_cart function
                elif choice == '7':
                    view_orders(customer[0])  # Pass CustomerID to view_orders function
                elif choice == '8':
                    manage_wallet(customer[0])  # Pass CustomerID to manage_wallet function
                elif choice == '9':
                    view_profile(customer[0])  # View profile option
                elif choice == '10':
                    print("Logging out...")
                    break
                else:
                    print("Invalid choice. Please enter a valid option.")
        else:
            # Increment login attempts
            cursor.execute("INSERT INTO LoginAttempts (email, attempts) VALUES (%s, 1) ON DUPLICATE KEY UPDATE attempts = attempts + 1", (email,))
            db_connection.commit()

            # Check if the user has reached the maximum login attempts
            cursor.execute("SELECT attempts FROM LoginAttempts WHERE email = %s", (email,))
            attempts = cursor.fetchone()[0]
            if attempts >= 3:
                # Lock the user out for 30 seconds
                lockout_until = datetime.datetime.now() + datetime.timedelta(seconds=30)
                cursor.execute("INSERT INTO LockedUsers (email, locked_until) VALUES (%s, %s) ON DUPLICATE KEY UPDATE locked_until = %s", (email, lockout_until, lockout_until))
                db_connection.commit()
                print(f"{email} is banned for 30 seconds. Try again after some time.")
                # Wait for 30 seconds before unban
                time.sleep(30)
                # Remove the ban
                cursor.execute("DELETE FROM LockedUsers WHERE email = %s", (email,))
                db_connection.commit()
            else:
                print("Invalid email or password.")
    except mysql.connector.Error as err:
        print("Error during login:", err)
    finally:
        cursor.close()



# Function to display filter options
def filter_menu():
    while True:
        print("\nFilter Search:")
        print("1. By Product Name")
        print("2. By Rating")
        print("3. By Price")
        print("4. Refundable Products")
        print("5. Back to Menu")
        choice = input("Enter your choice: ")
        if choice == '1':
            filter_by_name()
        elif choice == '2':
            filter_by_rating()
        elif choice == '3':
            filter_by_price()
        elif choice == '4':
            filter_by_refundable()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please enter a valid option.")


def view_wallet(customer_id):
    cursor = db_connection.cursor()
    query = "SELECT wallet FROM person WHERE person_id = %s"
    cursor.execute(query, (customer_id,))
    wallet_balance = cursor.fetchone()[0]
    cursor.close()
    print(f"Your current wallet balance is: ${wallet_balance:.2f}")

def add_money_to_wallet(customer_id):
    try:
        amount = float(input("Enter the amount to add to your wallet: "))
        if amount > 0:
            cursor = db_connection.cursor()
            update_query = "UPDATE person SET wallet = wallet + %s WHERE person_id = %s"
            cursor.execute(update_query, (amount, customer_id))
            db_connection.commit()
            cursor.close()
            print(f"${amount:.2f} added to your wallet successfully!")
        else:
            print("Amount must be greater than zero.")
    except ValueError:
        print("Invalid input for amount.")
    except mysql.connector.Error as err:
        print("Error adding money to wallet:", err)

def add_product(db_connection):
    try:
        # Get user input for product details
        product_name = input("Enter the product name: ")
        product_type = input("Enter the product type: ")
        product_price = float(input("Enter the product price: "))
        stock = int(input("Enter the stock: "))
        refundable_status = input("Is the product refundable? (yes/no): ")
        refundable_status = 1 if refundable_status.lower() == 'yes' else 0
        product_description = input("Enter the product description: ")

        # Start a transaction
        db_connection.start_transaction()

        # Insert new product into the database
        cursor = db_connection.cursor()
        insert_query = "INSERT INTO Product (ProductName, ProductType, ProductPrice, Stock, RefundableStatus, ProductDescription) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (product_name, product_type, product_price, stock, refundable_status, product_description))
        
        # Commit the transaction
        db_connection.commit()

        cursor.close()
        print("Product added successfully!")
    except ValueError:
        print("Invalid input for price or stock.")
    except mysql.connector.Error as err:
        print("Error adding product:", err)
        db_connection.rollback()  # Rollback the transaction on error



# Vendor login function
def vendor_login(dbconnection):
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    cursor = db_connection.cursor()
    try:
        # Check if the user is locked out
        cursor.execute("SELECT locked_until FROM LockedUsers WHERE email = %s", (email,))
        locked_until_time = cursor.fetchone()
        if locked_until_time and locked_until_time[0] > datetime.datetime.now():
            print("This email is banned. Try again after some time.")
            return

        query = "SELECT * FROM person WHERE email = %s AND password_ = %s"
        cursor.execute(query, (email, password))
        result = cursor.fetchone()

        if result:
            print("Login successful as Vendor!")

            while True:
                print("\nVendor Menu:")
                print("1. Add Products")
                print("2. Filter Search")
                print("3. view products")
                print("4. Logout")
                choice = input("Enter your choice: ")

                if choice == '1':
                    add_product(dbconnection)
                elif choice == '2':
                    filter_menu()
                elif choice == '3':
                    view_products()
                elif choice == '4':
                    print("Logging out...")
                    break
                else:
                    print("Invalid choice. Please enter a valid option.")

        else:
            # Increment login attempts
            cursor.execute("INSERT INTO LoginAttempts (email, attempts) VALUES (%s, 1) ON DUPLICATE KEY UPDATE attempts = attempts + 1", (email,))
            db_connection.commit()

            # Check if the user has reached the maximum login attempts
            cursor.execute("SELECT attempts FROM LoginAttempts WHERE email = %s", (email,))
            attempts = cursor.fetchone()[0]
            if attempts >= 3:
                # Lock the user out for 30 seconds
                lockout_until = datetime.datetime.now() + datetime.timedelta(seconds=30)
                cursor.execute("INSERT INTO LockedUsers (email, locked_until) VALUES (%s, %s) ON DUPLICATE KEY UPDATE locked_until = %s", (email, lockout_until, lockout_until))
                db_connection.commit()
                print(f"{email} is banned for 30 seconds. Try again after some time.")
                # Wait for 30 seconds before unban
                time.sleep(30)
                # Remove the ban
                cursor.execute("DELETE FROM LockedUsers WHERE email = %s", (email,))
                db_connection.commit()
            else:
                print("Invalid email or password.")
    except mysql.connector.Error as err:
        print("Error during login:", err)
    finally:
        cursor.close()

def buy_from_cart(customer_id, email):
    try:
        cursor = db_connection.cursor()

        # Start the transaction
        db_connection.start_transaction()

        # Retrieve all products from the cart
        cart_query = "SELECT ProductID, quantity FROM CART WHERE CustomerID = %s"
        cursor.execute(cart_query, (customer_id,))
        cart_items = cursor.fetchall()

        if cart_items:
            print("Products in your cart:")
            for item in cart_items:
                product_id, quantity = item
                print(f"Product ID: {product_id}, Quantity: {quantity}")

            insufficient_balance_count = 0  # Counter for insufficient balance messages

            while True:
                choice = input("Choose an option:\n1. Buy selectively\n2. Buy all from cart\n3. Back to Customer Menu\nEnter your choice: ")

                if choice == '1':
                    product_id = int(input("Enter the Product ID to buy: "))
                    cart_item = next((item for item in cart_items if item[0] == product_id), None)
                    if cart_item:
                        quantity_to_buy = cart_item[1]

                        # Check if the customer has sufficient balance
                        wallet_query = "SELECT wallet FROM person WHERE person_id = %s"
                        cursor.execute(wallet_query, (customer_id,))
                        wallet_balance = cursor.fetchone()[0]

                        if wallet_balance is not None:  
                            product_query = "SELECT ProductPrice, Stock FROM Product WHERE ProductID = %s"
                            cursor.execute(product_query, (product_id,))
                            product_data = cursor.fetchone()
                            product_price = product_data[0]
                            product_stock = product_data[1]

                            total_cost = product_price * quantity_to_buy

                            if wallet_balance >= total_cost:
                                # Deduct the amount from the wallet
                                update_wallet_query = "UPDATE person SET wallet = wallet - %s WHERE person_id = %s"
                                cursor.execute(update_wallet_query, (total_cost, customer_id))

                                # Insert the order into the Orders table
                                insert_order_query = "INSERT INTO Orders (CustomerID, ProductID, Quantity, Status_) VALUES (%s, %s, %s, 'Pending')"
                                cursor.execute(insert_order_query, (customer_id, product_id, quantity_to_buy))

                                # Decrease product stock
                                update_stock_query = "UPDATE Product SET Stock = Stock - %s WHERE ProductID = %s"
                                cursor.execute(update_stock_query, (quantity_to_buy, product_id))

                                # Remove the product from the cart
                                delete_cart_query = "DELETE FROM CART WHERE CustomerID = %s AND ProductID = %s"
                                cursor.execute(delete_cart_query, (customer_id, product_id))

                                print("Product bought successfully!")
                            else:
                                print("Insufficient balance.")
                                insufficient_balance_count += 1
                                if insufficient_balance_count > 3:
                                    # Lock the user out for 30 seconds
                                    lockout_until = datetime.datetime.now() + datetime.timedelta(seconds=30)
                                    cursor.execute("INSERT INTO LockedUsers (email, locked_until) VALUES (%s, %s) ON DUPLICATE KEY UPDATE locked_until = %s", (email, lockout_until, lockout_until))
                                    print(f"Account banned for 30 seconds due to multiple insufficient balance attempts.")
                                    time.sleep(30)
                                    # Remove the ban
                                    cursor.execute("DELETE FROM LockedUsers WHERE email = %s", (email,))
                                    insufficient_balance_count = 0  # Reset counter after unban

                        else:
                            print("Unable to retrieve wallet balance.")
                    else:
                        print("No such product found in your cart.")
                
                elif choice == '2':
                    total_cost = 0
                    for item in cart_items:
                        product_id, quantity_to_buy = item

                        # Get the price of the product
                        product_query = "SELECT ProductPrice, Stock FROM Product WHERE ProductID = %s"
                        cursor.execute(product_query, (product_id,))
                        product_data = cursor.fetchone()
                        product_price = product_data[0]
                        product_stock = product_data[1]

                        total_cost += product_price * quantity_to_buy

                    # Check if the customer has sufficient balance for all items
                    wallet_query = "SELECT wallet FROM person WHERE person_id = %s"
                    cursor.execute(wallet_query, (customer_id,))
                    wallet_balance = cursor.fetchone()[0]

                    if wallet_balance is not None and wallet_balance >= total_cost:
                        for item in cart_items:
                            product_id, quantity_to_buy = item

                            # Insert the order into the Orders table
                            insert_order_query = "INSERT INTO Orders (CustomerID, ProductID, Quantity, Status_) VALUES (%s, %s, %s, 'Pending')"
                            cursor.execute(insert_order_query, (customer_id, product_id, quantity_to_buy))

                            # Decrease product stock
                            update_stock_query = "UPDATE Product SET Stock = Stock - %s WHERE ProductID = %s"
                            cursor.execute(update_stock_query, (quantity_to_buy, product_id))

                        # Deduct the total amount from the wallet
                        update_wallet_query = "UPDATE person SET wallet = wallet - %s WHERE person_id = %s"
                        cursor.execute(update_wallet_query, (total_cost, customer_id))

                        # Clear the cart
                        delete_cart_query = "DELETE FROM CART WHERE CustomerID = %s"
                        cursor.execute(delete_cart_query, (customer_id,))

                        print("All products bought successfully!")
                    else:
                        print("Insufficient balance to buy all products in the cart.")
                        insufficient_balance_count += 1
                        if insufficient_balance_count > 3:
                            # Lock the user out for 30 seconds
                            lockout_until = datetime.datetime.now() + datetime.timedelta(seconds=30)
                            cursor.execute("INSERT INTO LockedUsers (email, locked_until) VALUES (%s, %s) ON DUPLICATE KEY UPDATE locked_until = %s", (email, lockout_until, lockout_until))
                            print(f"Account banned for 30 seconds due to multiple insufficient balance attempts.")
                            time.sleep(30)
                            # Remove the ban
                            cursor.execute("DELETE FROM LockedUsers WHERE email = %s", (email,))
                            insufficient_balance_count = 0  # Reset counter after unban

                elif choice == '3':
                    # Return to Customer Menu
                    break  # Exit the loop and return to the customer menu

                else:
                    print("Invalid choice.")
        else:
            print("No products found in your cart.")

        # Commit the transaction
        db_connection.commit()

    except ValueError:
        print("Invalid input for Product ID.")
    except mysql.connector.Error as err:
        print("Error:", err)
        # Rollback the transaction in case of error
        db_connection.rollback()
    finally:
        cursor.close()




 #Customer signup function
def customer_signup(db_connection):
    try:
        # Get user input for customer details
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        phone_no = input("Enter your phone number: ")
        email = input("Enter your email: ")
        street_id = input("Enter your street ID: ")
        city = input("Enter your city: ")
        landmark = input("Enter your landmark: ")
        state = input("Enter your state: ")
        pincode = input("Enter your pincode: ")
        dob = input("Enter your date of birth (YYYY-MM-DD): ")
        password = input("Set your password: ")

        # Email constraint check
        if '@' not in email:
            raise ValueError("Invalid email format")

        # Password constraint check
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")

        # Pin code constraint check
        if len(pincode) != 6:
            raise ValueError("Pin code must be 6 characters long")

        # Phone number constraint check
        if not (0 < int(phone_no) <= 9999999999):
            raise ValueError("Invalid phone number")

        # Start a transaction
        db_connection.start_transaction()

        # Inserting new customer into the database
        cursor = db_connection.cursor()
        # Check if the email already exists
        email_check_query = "SELECT person_id FROM person WHERE email = %s"
        cursor.execute(email_check_query, (email,))
        if cursor.fetchone():
            raise ValueError("Email already exists")
        
        insert_query = "INSERT INTO person (first_name, last_name, phone_no, email, street_id, city, landmark, states, pincode, dob, password_) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (first_name, last_name, phone_no, email, street_id, city, landmark, state, pincode, dob, password))

        # Get the person_id of the newly inserted person
        person_id = cursor.lastrowid

        # Inserting customer data into the customer table
        insert_customer_query = "INSERT INTO customer (person_id, NumberOfOrdersPlaced) VALUES (%s, %s)"
        cursor.execute(insert_customer_query, (person_id, 0))  # Defaulting NumberOfOrdersPlaced to 0

        db_connection.commit()  # Commit the transaction

        cursor.close()
        print("Signup successful as Customer!")
    except ValueError as ve:
        print("Error during signup:", ve)
        db_connection.rollback()  # Rollback the transaction on error
    except mysql.connector.Error as err:
        print("Error during signup:", err)
        db_connection.rollback()  # Rollback the transaction on error





# Vendor signup function
def vendor_signup(dbconnection):
    try:
        # Start transaction
        db_connection.start_transaction()

        # Get user input for vendor details
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        phone_no = input("Enter your phone number: ")
        email = input("Enter your email: ")
        street_id = input("Enter your street ID: ")
        city = input("Enter your city: ")
        landmark = input("Enter your landmark: ")
        state = input("Enter your state: ")
        pincode = input("Enter your pincode: ")
        dob = input("Enter your date of birth (YYYY-MM-DD): ")
        password = input("Set your password: ")

        # Email constraint check
        if '@' not in email:
            raise ValueError("Invalid format")

        # Password constraint check
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")

        # Pin code constraint check
        if len(pincode) != 6:
            raise ValueError("Pin code must be 6 characters long")

        # Phone number constraint check
        if not (0 < int(phone_no) <= 9999999999):
            raise ValueError("Invalid phone number")

        # Inserting new vendor into the database
        cursor = db_connection.cursor()
        insert_query = "INSERT INTO person (first_name, last_name, phone_no, email, street_id, city, landmark, states, pincode, dob, password_) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (first_name, last_name, phone_no, email, street_id, city, landmark, state, pincode, dob, password))
        cursor.close()
        print("Signup successful as Vendor!")

        # Commit transaction if successful
        db_connection.commit()

    except ValueError as ve:
        print("Error during signup:", ve)
        # Rollback transaction on error
        db_connection.rollback()
    except mysql.connector.Error as err:
        print("Error during signup:", err)
        # Rollback transaction on error
        db_connection.rollback()

    finally:
        # Close database connection
        db_connection.close()

# Vendor menu
def vendor_menu(dbconnection):
    while True:
        print("\nVendor Menu:")
        print("1. Login")
        print("2. Signup")
        print("3. Back to main menu")
        choice = input("Enter your choice: ")
        if choice == '1':
            vendor_login(dbconnection)
        elif choice == '2':
            vendor_signup(dbconnection)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please enter a valid option.")

def admin_login():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    if email == 'admin123@gmail.com' and password == 'admin123':
        print("Login successful as Admin!")
        admin_menu()
        
    else:
        print("Invalid email or password.")


def admin_menu():
    while True:
        print("\nAdmin Menu:")
        print("1. View Members")
        print("2. View Member History")
        print("3. View Employees")
        print("4. View Managers")
        print("5. Remove Employee")
        print("6. Remove Manager")
        print("7. Add Employee")
        print("8. Add Manager")
        print("9. Logout")
        choice = input("Enter your choice: ")
        if choice == '1':
            view_members()
        elif choice == '2':
            view_member_history()
        elif choice == '3':
            view_employees()
        elif choice == '4':
            view_managers()
        elif choice == '5':
            remove_employee()
        elif choice == '6':
            remove_manager()
        elif choice == '7':
            add_employee()
        elif choice == '8':
            add_manager()
        elif choice == '9':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")


# Function to add an employee
def add_employee():
    try:
        # Get user input for employee details
        first_name = input("Enter employee's first name: ")
        middle_name = input("Enter employee's middle name: ")
        if not middle_name:  
            middle_name = None  
        last_name = input("Enter employee's last name: ")
        manager_id = int(input("Enter Manager ID: "))
        employee_contact = input("Enter employee's contact number: ")
        employee_email = input("Enter employee's email: ")
        joining_date = input("Enter employee's joining date (YYYY-MM-DD): ")
        position = input("Enter employee's position: ")

        # Check if the ManagerID exists in the database
        cursor = db_connection.cursor()
        query = "SELECT * FROM Manager WHERE ManagerID = %s"
        cursor.execute(query, (manager_id,))
        manager = cursor.fetchone()
        if manager:
            insert_query = "INSERT INTO Employee (FirstName, MiddleName, LastName, ManagerID, EmployeeContact, EmployeeEmail, JoiningDate, Position_) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (first_name, middle_name, last_name, manager_id, employee_contact, employee_email, joining_date, position))
            db_connection.commit()
            cursor.close()
            print("Employee added successfully!")
        else:
            print("Manager with ID {} does not exist.".format(manager_id))
    except ValueError:
        print("Invalid input for Manager ID.")
    except mysql.connector.Error as err:
        print("Error adding employee:", err)
        cursor.close()

def add_manager():
    try:

        first_name = input("Enter manager's first name: ")
        middle_name = input("Enter manager's middle name (press Enter if none): ")
        if not middle_name:  
            middle_name = None 
        last_name = input("Enter manager's last name: ")
        manager_contact = input("Enter manager's contact number: ")
        manager_email = input("Enter manager's email: ")
        branch_id = int(input("Enter Branch ID: "))


        cursor = db_connection.cursor()
        insert_query = "INSERT INTO Manager (FirstName, MiddleName, LastName, ManagerContact, ManagerEmail, BranchID) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (first_name, middle_name, last_name, manager_contact, manager_email, branch_id))
        db_connection.commit()
        cursor.close()
        print("Manager added successfully!")
    except ValueError:
        print("Invalid input for Branch ID.")
    except mysql.connector.Error as err:
        print("Error adding manager:", err)


def remove_manager():
    try:
        # Start transaction
        db_connection.start_transaction()

        manager_id = int(input("Enter the Manager ID to remove: "))
        cursor = db_connection.cursor()

        query = "SELECT * FROM Manager WHERE ManagerID = %s"
        cursor.execute(query, (manager_id,))
        manager = cursor.fetchone()

        if manager:
            # Get another manager ID to reassign employees, if available
            cursor.execute("SELECT ManagerId FROM Manager WHERE ManagerId <> %s LIMIT 1", (manager_id,))
            new_manager_id = cursor.fetchone()
            
            if new_manager_id:
                # Update Employee table to reassign employees to another manager
                cursor.execute("UPDATE Employee SET ManagerId = %s WHERE ManagerId = %s", (new_manager_id[0], manager_id))
            else:
                print("Please first assign at least 1 manager.")

            # Delete manager
            delete_query = "DELETE FROM Manager WHERE ManagerID = %s"
            cursor.execute(delete_query, (manager_id,))
            db_connection.commit()
            print("Manager removed successfully!")
        else:
            print("Manager not found.")
    except ValueError:
        print("Invalid input for Manager ID.")
    except mysql.connector.Error as err:
        print("Error:", err)
        # Rollback transaction on error
        db_connection.rollback()
    finally:
        cursor.close()


def remove_employee():
    try:
        # Start transaction
        db_connection.start_transaction()

        employee_id = int(input("Enter the Employee ID to remove: "))
        cursor = db_connection.cursor()
        query = "SELECT * FROM Employee WHERE EmployeeID = %s"
        cursor.execute(query, (employee_id,))
        employee = cursor.fetchone()

        if employee:
            # Delete associated records from other tables
            cursor.execute("DELETE FROM orderids WHERE EmployeeID = %s", (employee_id,))
            cursor.execute("DELETE FROM productids WHERE EmployeeID = %s", (employee_id,))
            
            # Delete employee from the Employee table
            delete_query = "DELETE FROM Employee WHERE EmployeeID = %s"
            cursor.execute(delete_query, (employee_id,))
            db_connection.commit()
            print("Employee removed successfully!")
        else:
            print("Employee not found.")
    except ValueError:
        print("Invalid input for Employee ID.")
    except mysql.connector.Error as err:
        print("Error:", err)
        # Rollback transaction on error
        db_connection.rollback()
    finally:
        cursor.close()



def view_managers():
    cursor = db_connection.cursor()
    query = "SELECT * FROM Manager"
    cursor.execute(query)
    managers = cursor.fetchall()
    cursor.close()

    print("All Managers:")
    for manager in managers:
        print(manager)


def view_employees():
    cursor = db_connection.cursor()
    query = "SELECT * FROM Employee"
    cursor.execute(query)
    employees = cursor.fetchall()
    cursor.close()

    print("All Employees:")
    for employee in employees:
        print(employee)


def view_member_history():
    member_id = input("Enter the member ID: ")
    cursor = db_connection.cursor()
    query = "SELECT * FROM CustomerHistory AS CH WHERE CH.CustomerID = %s"
    cursor.execute(query, (member_id,))
    member_history = cursor.fetchall()
    cursor.close()

    if member_history:
        print(f"History for Member ID {member_id}:")
        for history in member_history:
            order_date = history[0]
            payment = history[1]
            orderstatus = history[2]
            productType = history[4]
            print(f"{order_date} {productType} {payment} {orderstatus}")
    else:
        print("No history found for the member ID.")


def view_members():
    cursor = db_connection.cursor()
    query = "SELECT * FROM person"
    cursor.execute(query)
    members = cursor.fetchall()
    cursor.close()

    print("All Members:")
    for member in members:
        print(member)
            

# Run the main menu
main_menu(db_connection)

# Close the database connection
db_connection.close()