# Data-Base-Management-System
User Guide for SQL Database CLI

Establishing a Database Connection
- Description: Connects to a MySQL database named GIFTSTORE.
- Details: Uses localhost as the host, with root as the username and a specified password.
- Usage: Automatically established when the script is run.

View Orders
- Description: Allows users to view all orders associated with a given customer ID.
- Function Call: view_orders(customer_id)
- Parameters:
  - customer_id: Integer representing the unique ID of the customer.
- Output: Displays each order for the customer, including Order ID, Product Name, Quantity, and Status.
- Usage Example:
  
  view_orders(123)
  

View Products
- Description: Fetches and displays all products from the database.
- Function Call: view_products()
- Output: Lists each product with its ID and name.
- Usage Example:
  
  view_products()
  

Filter Products by Name
- Description: Filters and displays products based on a search term included in the product name.
- Function Call: filter_by_name()
- Input: User prompted to enter the product name or part of it they wish to search for.
- Output: Lists products matching the search criteria.
- Usage Example:
  
  filter_by_name()
  

Filter Products by Rating
- Description: Allows users to filter products by a minimum star rating.
- Function Call: filter_by_rating()
- Input: User prompted to enter the minimum star rating (between 1 and 5).
- Output: Displays products that meet or exceed the specified rating.
- Usage Example:
  
  filter_by_rating()
  

Filter Products by Price
- Description: Filters and displays products that have a price greater than or equal to a specified amount.
- Function Call: filter_by_price()
- Input: User prompted to enter the minimum price.
- Output: Lists products with prices that are at or above the specified price.
- Usage Example:
  
  filter_by_price()
  

View Managers
- Description: Displays a list of all managers in the database.
- Function Call: view_managers()
- Output: Lists each manager with associated details.
- Usage Example:
  
  view_managers()
  

View Employees
- Description: Fetches and displays information about all employees.
- Function Call: view_employees()
- Output: Displays details of all employees.
- Usage Example:
  
  view_employees()
  

View Member History
- Description: Retrieves and displays the transaction history of a specified member.
- Function Call: view_member_history()
- Input: User prompted to enter the member ID.
- Output: Displays the transaction history of the member, including order dates, payments, and statuses.
- Usage Example:
  
  view_member_history()
  

View Members
- Description: Lists all members in the database.
- Function Call: view_members()
- Output: Shows details of each member.
- Usage Example:
  
  view_members()
  

Purchase Products from Cart
- Description: Allows customers to purchase products added to their cart. Checks for sufficient balance, updates wallet, places orders, updates stock, and clears the cart.
- Details: Integrated into the CLI menu where the customer selects the purchase option after adding products to their cart.
