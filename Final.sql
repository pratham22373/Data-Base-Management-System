CREATE DATABASE GIFTSTORE;

USE GIFTSTORE;

CREATE TABLE person (
    person_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    last_name VARCHAR(50) NOT NULL,
    phone_no BIGINT UNSIGNED NOT NULL,
    email VARCHAR(255) NOT NULL,
    street_id VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    landmark VARCHAR(255) NOT NULL,
    states VARCHAR(255) NOT NULL,
    pincode INT UNSIGNED NOT NULL,
    dob DATE NOT NULL,
    password_ VARCHAR(25) NOT NULL,
    wallet DECIMAL(10, 2) DEFAULT 0, -- Adding the wallet column with default value 0
    CONSTRAINT chk_person_email CHECK (email LIKE '%@%'), 
    CONSTRAINT chk_person_password_length CHECK (LENGTH(password_) >= 6), 
    CONSTRAINT chk_person_pincode_length CHECK (LENGTH(pincode) = 6),
    CONSTRAINT chk_person_phone CHECK (phone_no > 0 AND phone_no <= 9999999999)
);




INSERT INTO person (first_name, middle_name, last_name, phone_no, email, street_id, city, landmark, states, pincode, dob, password_, wallet)
VALUES
('John', NULL, 'Doe', 1234567890, 'john.doe@example.com', '123 Street', 'Cityville', 'Near Park', 'State A', 123456, '1990-01-01', 'password123', 1000),
('Jane', 'Mary', 'Smith', 9876543210, 'jane.smith@example.com', '456 Avenue', 'Townsville', 'Next to School', 'State B', 654321, '1995-05-15', 'secret@123', NULL),
('Alice', 'Elizabeth', 'Johnson', 5555555555, 'alice.johnson@example.com', '789 Road', 'Villageton', 'Opposite Market', 'State C', 456789, '1988-07-20', 'securepass', NULL),
('Bob', NULL, 'Brown', 7777777777, 'bob.brown@example.com', '101 Main Street', 'Metropolis', 'Beside Library', 'State D', 333333, '1975-11-30', 'mypassword', 1000),
('Emily', 'Grace', 'Taylor', 9999999999, 'emily.taylor@example.com', '789 Elm Avenue', 'Smalltown', 'Near Post Office', 'State E', 444444, '1999-03-10', 'password1234', NULL),
('Michael', NULL, 'Clark', 1111111111, 'michael.clark@example.com', '222 Oak Street', 'Hometown', 'By the River', 'State F', 555555, '1992-09-05', 'letmein12', 3565),
('Sophia', 'Rose', 'Martinez', 2222222222, 'sophia.martinez@example.com', '456 Maple Lane', 'Citytown', 'Near Hospital', 'State G', 777777, '1980-04-25', 'pass123word', 3434),
('William', 'James', 'Anderson', 3333333333, 'william.anderson@example.com', '888 Pine Road', 'Uptown', 'By the Lake', 'State H', 888888, '1983-12-15', 'secure123', NULL),
('Olivia', NULL, 'White', 4444444444, 'olivia.white@example.com', '999 Birch Boulevard', 'Downtown', 'Next to Stadium', 'State I', 999999, '1972-06-18', 'password!@#', 4323),
('Daniel', 'Thomas', 'Lee', 5555555555, 'daniel.lee@example.com', '777 Cedar Street', 'Suburbia', 'Near School', 'State J', 111111, '1986-08-08', '12345678', NULL),
('Ava', NULL, 'Harris', 6666666666, 'ava.harris@example.com', '333 Fir Lane', 'Outskirts', 'Near Farm', 'State K', 222222, '1996-02-28', 'pass123', 435432),
('James', 'Robert', 'Evans', 7777777777, 'james.evans@example.com', '555 Pine Lane', 'Countryside', 'By the Woods', 'State L', 333333, '1978-10-12', 'letmein', NULL),
('Mia', 'Emma', 'Wilson', 8888888888, 'mia.wilson@example.com', '111 Oak Boulevard', 'Village', 'Next to Church', 'State M', 444444, '1993-04-17', 'password1', 32435),
('Alexander', 'David', 'Thomas', 9999999999, 'alexander.thomas@example.com', '222 Maple Street', 'Rural', 'Near River', 'State N', 555555, '1989-11-23', '123456789', NULL),
('Charlotte', NULL, 'Walker', 1234567890, 'charlotte.walker@example.com', '999 Elm Lane', 'Hamlet', 'By the Mill', 'State O', 666666, '1970-08-05', 'abc123', NULL);



CREATE TABLE vendor(

    person_id INT,
    FOREIGN KEY (person_id) REFERENCES person (person_id) on delete cascade,
    vendor_id INT NOT NULL PRIMARY KEY auto_increment,
    shop_type VARCHAR(255) NOT NULL ,
    Rating DECIMAL(3, 2) NOT NULL,
    CONSTRAINT chk_vendor_rating_range CHECK (Rating >= 0 AND Rating <= 5) -- Ensure rating is between 0 and 5
 );
 
 INSERT INTO vendor (person_id, shop_type, Rating) VALUES
-- Cakes
(1, 'Cakes', 4.5),
(2, 'Cakes', 4.2),
(3, 'Cakes', 4.6),
-- Flowers
(4, 'Flowers', 4.3),
(5, 'Flowers', 4.7),
(6, 'Flowers', 4.0),
-- Personalised Gifts
(7, 'Personalised Gifts', 4.1),
(8, 'Personalised Gifts', 4.8),
(9, 'Personalised Gifts', 4.4),
-- Chocolates
(10, 'Chocolates', 4.9),
(11, 'Chocolates', 4.3),
(12, 'Chocolates', 4.6),
-- Plants
(13, 'Plants', 4.2),
(14, 'Plants', 4.7),
(15, 'Plants', 4.5);


CREATE TABLE customer(

    person_id INT,
    FOREIGN KEY (person_id) REFERENCES person (person_id) on delete cascade,
    customer_id INT NOT NULL PRIMARY KEY auto_increment,
    NumberOfOrdersPlaced INT NOT NULL DEFAULT 0, -- Default to 0
    CONSTRAINT chk_orders_placed CHECK (NumberOfOrdersPlaced >= 0) -- Ensure non-negative orders placed
);

INSERT INTO customer (person_id, NumberOfOrdersPlaced) VALUES
(1, 3),
(2, 7),
(3, 1),
(4, 10),
(5, 5),
(6, 2),
(7, 8),
(8, 4),
(9, 6),
(10, 9),
(11, 3),
(12, 5),
(13, 2),
(14, 7),
(15, 4);


CREATE TABLE Product (
    ProductID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    ProductName VARCHAR(255) NOT NULL,
    ProductType VARCHAR(255) NOT NULL,
    ProductPrice DECIMAL(10, 2) NOT NULL,
    Stock INT NOT NULL DEFAULT 0,
    RefundableStatus BOOLEAN NOT NULL,
    ProductDescription TEXT NOT NULL,
    Stars FLOAT NOT NULL DEFAULT 0, -- Default value set to 0
    vendor_id INT,
    CONSTRAINT chk_product_price_positive CHECK (ProductPrice >= 0),
    CONSTRAINT chk_stock_non_negative CHECK (Stock >= 0),
    CONSTRAINT chk_stars_range CHECK (Stars >= 0 AND Stars <= 5),
    FOREIGN KEY (vendor_id) REFERENCES vendor (vendor_ID) ON DELETE CASCADE
);

INSERT INTO Product (ProductName, ProductType, ProductPrice, Stock, RefundableStatus, ProductDescription, Stars, vendor_id) VALUES
('Red Roses Bouquet', 'Flowers', 29.99, 1, TRUE, 'A beautiful bouquet of red roses.', 4.5, 1),
('Custom Engraved Necklace', 'Personalised Gifts', 49.99, 30, TRUE, 'A necklace with a custom engraving.', 4.8, 2),
('Assorted Chocolates Box', 'Chocolates', 19.99, 100, TRUE, 'A selection of various chocolates.', 4.3, 3),
('Potted Succulent Plant', 'Plants', 24.99, 20, TRUE, 'A small potted succulent plant.', 4.2, 4),
('Mixed Flowers and Cake Combo', 'Flowers N Cakes', 39.99, 40, TRUE, 'A combo of flowers and a cake.', 4.6, 5),
('Gift Hamper with Wine', 'Gift Hampers', 79.99, 10, TRUE, 'A gift hamper including wine and snacks.', 4.7, 6),
('Flowers and Chocolates Combo', 'Flowers N Chocolates', 34.99, 25, TRUE, 'A combo of flowers and chocolates.', 4.4, 7),
('Orchid Plant', 'Plants', 29.99, 15, TRUE, 'A potted orchid plant.', 4.1, 8),
('Customized Mug', 'Personalised Gifts', 14.99, 60, TRUE, 'A mug with custom printing.', 4.6, 9),
('Assorted Snacks Combo', 'Combos', 49.99, 35, TRUE, 'A combo of assorted snacks.', 4.2, 10),
('Bouquet of Lilies', 'Flowers', 39.99, 30, TRUE, 'A bouquet of lilies.', 4.3, 11),
('Chocolate Cake', 'Chocolates', 29.99, 20, TRUE, 'A delicious chocolate cake.', 4.8, 12),
('Plants and Chocolates Combo', 'Combos', 49.99, 25, TRUE, 'A combo of plants and chocolates.', 4.5, 13),
('Luxury Gift Basket', 'Gift Hampers', 99.99, 5, TRUE, 'A luxurious gift basket with various items.', 4.9, 14),
('Assorted Flowers Bouquet', 'Flowers', 49.99, 40, TRUE, 'A bouquet of assorted flowers.', 4.7, 15);


CREATE TABLE VendorHistory (

    SellingDate DATE NOT NULL,
	ProductID INT,
    ProductQuantity INT NOT NULL ,
    OrderStatus VARCHAR(255) NOT NULL,
    VendorID INT ,
    -- ProductType VARCHAR(255) NOT NULL,
	FOREIGN KEY (ProductID) REFERENCES Product (ProductID),
    FOREIGN KEY (VendorID) REFERENCES vendor (vendor_ID),
    CONSTRAINT chk_product_quantity_positive CHECK (ProductQuantity > 0), -- Ensure positive product quantity
    CONSTRAINT chk_vendor_order_status CHECK (OrderStatus IN ('Pending', 'Processing', 'Shipped', 'Delivered')) -- Ensure valid order status
);

INSERT INTO VendorHistory (SellingDate, ProductID, ProductQuantity, OrderStatus, VendorID) VALUES
('2024-02-01', 1, 5, 'Delivered', 1),
('2024-02-02', 2, 3, 'Shipped', 2),
('2024-02-03', 3, 7, 'Processing', 3),
('2024-02-04', 4, 2, 'Pending', 4),
('2024-02-05', 5, 6, 'Delivered', 5),
('2024-02-06', 6, 4, 'Shipped', 6),
('2024-02-07', 7, 8, 'Delivered', 7),
('2024-02-08', 8, 1, 'Shipped', 8),
('2024-02-09', 9, 3, 'Delivered', 9),
('2024-02-10', 10, 5, 'Processing', 10),
('2024-02-11', 11, 2, 'Pending', 11),
('2024-02-12', 12, 4, 'Processing', 12),
('2024-02-13', 13, 6, 'Delivered', 13),
('2024-02-14', 14, 7, 'Shipped', 14),
('2024-02-15', 15, 3, 'Delivered', 15);


CREATE TABLE CART (

	CustomerID INT NOT NULL,
    FOREIGN KEY (CustomerID) REFERENCES customer (customer_id) on delete cascade,
    ProductID INT NOT NULL,
    FOREIGN KEY (ProductID) REFERENCES Product (ProductID),
    quantity INT,
    check (quantity>0)
);

INSERT INTO CART (CustomerID, ProductID, Quantity) VALUES
(1, 1, 2),
(1, 3, 1),
(2, 2, 3),
(2, 5, 2),
(3, 4, 1),
(4, 6, 2),
(4, 8, 1),
(5, 10, 3),
(6, 12, 1),
(6, 14, 2),
(7, 3, 1),
(8, 5, 2),
(9, 7, 1),
(9, 9, 2),
(10, 11, 1);


CREATE TABLE Review (

    ReviewID INT PRIMARY KEY NOT NULL auto_increment,
    Date_ DATE NOT NULL,
    Content TEXT NOT NULL,
    ProductID INT NOT NULL,
    FOREIGN KEY (ProductID) REFERENCES Product (ProductID) on delete cascade,
    Customer_ID INT NOT NULL,
    FOREIGN KEY (Customer_ID) REFERENCES customer (customer_id) 
);

INSERT INTO Review (Date_, Content, ProductID, Customer_ID) VALUES
('2024-01-01', 'Great product, highly recommended.', 1, 1),
('2024-01-02', 'The personalized gift was perfect!', 2, 2),
('2024-01-03', 'Delicious chocolates, fast delivery.', 3, 3),
('2024-01-04', 'Beautiful plant, exceeded my expectations.', 4, 4),
('2024-01-05', 'Flowers and cake combo was a hit at the party.', 5, 5),
('2024-01-06', 'The gift hamper was well-packaged and had a great selection.', 6, 6),
('2024-01-07', 'Lovely flowers and chocolates, thank you!', 7, 7),
('2024-01-08', 'The orchid plant arrived in perfect condition.', 8, 8),
('2024-01-09', 'The customized mug was exactly what I wanted.', 9, 9),
('2024-01-10', 'Great combo of assorted snacks, loved it!', 10, 10),
('2024-01-11', 'Lilies bouquet was fresh and fragrant.', 11, 1),
('2024-01-12', 'Chocolate cake was a big hit at the event.', 12, 2),
('2024-01-13', 'Plants and chocolates combo was a unique gift.', 13, 3),
('2024-01-14', 'Luxury gift basket had high-quality items.', 14, 4),
('2024-01-15', 'Assorted flowers bouquet was beautifully arranged.', 15, 5);


CREATE TABLE Orders (

    OrderID INT PRIMARY KEY NOT NULL auto_increment,
    CustomerID INT NOT NULL,
    FOREIGN KEY (CustomerID) REFERENCES customer (customer_id),
    ProductID INT NOT NULL,
    FOREIGN KEY (ProductID) REFERENCES Product (ProductID),
    Quantity INT NOT NULL DEFAULT 1, -- Default to 1
    Status_ VARCHAR(255) NOT NULL,
    CONSTRAINT chk_order_quantity_positive CHECK (Quantity > 0), -- Ensure positive quantity
    CONSTRAINT chk_order_status CHECK (Status_ IN ('Pending', 'Processing', 'Shipped', 'Delivered')) -- Ensure valid status
);

INSERT INTO Orders (CustomerID, ProductID, Quantity, Status_) VALUES
(1, 1, 2, 'Pending'),
(2, 2, 1, 'Processing'),
(3, 3, 3, 'Shipped'),
(4, 4, 1, 'Delivered'),
(5, 5, 2, 'Pending'),
(6, 6, 1, 'Processing'),
(7, 7, 3, 'Shipped'),
(8, 8, 1, 'Delivered'),
(9, 9, 2, 'Pending'),
(10, 10, 1, 'Processing'),
(11, 11, 3, 'Shipped'),
(12, 12, 1, 'Delivered'),
(13, 13, 2, 'Pending'),
(14, 14, 1, 'Processing'),
(15, 15, 3, 'Shipped');

CREATE TABLE Delivery (

    DeliveryID INT PRIMARY KEY NOT NULL auto_increment,
    OrderID INT NOT NULL,
    FOREIGN KEY (OrderID) REFERENCES Orders (OrderID) on delete cascade,
    Status_ VARCHAR(255) NOT NULL,
    EstimatedTime TIME NOT NULL,
    CONSTRAINT chk_delivery_status CHECK (Status_ IN ('Scheduled', 'In transit', 'Out for delivery', 'Delivered')) -- Ensure valid status
);

INSERT INTO Delivery (OrderID, Status_, EstimatedTime) VALUES
(1, 'Scheduled', '08:00:00'),
(2, 'In transit', '10:30:00'),
(3, 'Out for delivery', '12:45:00'),
(4, 'Delivered', '14:15:00'),
(5, 'Scheduled', '09:30:00'),
(6, 'In transit', '11:00:00'),
(7, 'Out for delivery', '13:15:00'),
(8, 'Delivered', '15:00:00'),
(9, 'Scheduled', '10:00:00'),
(10, 'In transit', '12:30:00'),
(11, 'Out for delivery', '14:45:00'),
(12, 'Delivered', '16:30:00'),
(13, 'Scheduled', '11:30:00'),
(14, 'In transit', '13:45:00'),
(15, 'Out for delivery', '15:30:00');


CREATE TABLE payment (
    TransactionID INT PRIMARY KEY NOT NULL auto_increment,
    OrderID INT NOT NULL,
    FOREIGN KEY (OrderID) REFERENCES Orders (OrderID) ON DELETE CASCADE,
    PaymentType VARCHAR(50) NOT NULL,
    Status_ VARCHAR(50) NOT NULL CHECK (Status_ IN ('Successful', 'Pending', 'Failed')),
    Amount DECIMAL(10, 2) NOT NULL,
    ProductPrice DECIMAL(10, 2) NOT NULL,
    DeliveryCharge DECIMAL(10, 2) NOT NULL,
    Discount DECIMAL(10, 2) NOT NULL,
    CONSTRAINT chk_amount_positive CHECK (Amount >= 0),
    CONSTRAINT chk_product_price_pos CHECK (ProductPrice >= 0),
    CONSTRAINT chk_delivery_charge_positive CHECK (DeliveryCharge >= 0),
    CONSTRAINT chk_discount_non_negative CHECK (Discount >= 0)
);

INSERT INTO payment (OrderID, PaymentType, Status_, Amount, ProductPrice, DeliveryCharge, Discount) VALUES
(1, 'Credit Card', 'Successful', 100.00, 90.00, 5.00, 0.00),
(2, 'PayPal', 'Pending', 150.00, 140.00, 8.00, 2.00),
(3, 'Debit Card', 'Successful', 80.00, 70.00, 6.00, 4.00),
(4, 'Cash on Delivery', 'Failed', 200.00, 180.00, 10.00, 10.00),
(5, 'Credit Card', 'Pending', 120.00, 110.00, 7.00, 3.00),
(6, 'PayPal', 'Successful', 90.00, 80.00, 5.00, 0.00),
(7, 'Credit Card', 'Failed', 250.00, 230.00, 15.00, 5.00),
(8, 'Debit Card', 'Successful', 110.00, 100.00, 8.00, 2.00),
(9, 'Cash on Delivery', 'Pending', 140.00, 130.00, 7.00, 3.00),
(10, 'PayPal', 'Successful', 70.00, 60.00, 5.00, 0.00),
(11, 'Credit Card', 'Failed', 180.00, 160.00, 10.00, 10.00),
(12, 'Debit Card', 'Pending', 200.00, 190.00, 8.00, 2.00),
(13, 'Cash on Delivery', 'Successful', 150.00, 140.00, 9.00, 1.00),
(14, 'PayPal', 'Successful', 130.00, 120.00, 6.00, 4.00),
(15, 'Credit Card', 'Pending', 100.00, 90.00, 7.00, 3.00);


CREATE TABLE CustomerHistory (

    OrderDate DATE NOT NULL,
    Payment DECIMAL(10, 2) NOT NULL,
    OrderStatus VARCHAR(255) NOT NULL,
    CustomerID INT NOT NULL,
    FOREIGN KEY (CustomerID) REFERENCES customer (customer_id) ON DELETE CASCADE,
    ProductType VARCHAR(255) NOT NULL,
    CONSTRAINT chk_payment_non_negative CHECK (Payment >= 0), -- Ensure non-negative payment
    CONSTRAINT chk_customer_order_status CHECK (OrderStatus IN ('Pending', 'Processing', 'Shipped', 'Delivered')) -- Ensure valid order status
);

INSERT INTO CustomerHistory (OrderDate, Payment, OrderStatus, CustomerID, ProductType) VALUES
('2024-01-01', 100.00, 'Delivered', 1, 'Cakes'),
('2024-01-02', 150.00, 'Shipped', 2, 'Flowers'),
('2024-01-03', 80.00, 'Processing', 3, 'Personalised Gifts'),
('2024-01-04', 200.00, 'Pending', 4, 'Chocolates'),
('2024-01-05', 120.00, 'Delivered', 5, 'Plants'),
('2024-01-06', 90.00, 'Shipped', 6, 'Flowers N Cakes'),
('2024-01-07', 250.00, 'Delivered', 7, 'Combos'),
('2024-01-08', 110.00, 'Shipped', 8, 'Gift Hampers'),
('2024-01-09', 140.00, 'Delivered', 9, 'Flowers N Chocolates'),
('2024-01-10', 70.00, 'Processing', 10, 'Cakes'),
('2024-01-11', 180.00, 'Pending', 11, 'Flowers'),
('2024-01-12', 200.00, 'Processing', 12, 'Personalised Gifts'),
('2024-01-13', 150.00, 'Delivered', 13, 'Chocolates'),
('2024-01-14', 130.00, 'Shipped', 14, 'Plants'),
('2024-01-15', 100.00, 'Delivered', 15, 'Flowers N Cakes');


CREATE TABLE Branch (
    BranchID INT PRIMARY KEY NOT NULL auto_increment,
    -- ManagerID INT NOT NULL,
    StreetID INT NOT NULL,
    City VARCHAR(100) NOT NULL,
    LandMark VARCHAR(100),
    State VARCHAR(100) NOT NULL,
    Pincode INT NOT NULL,
    BranchContact BIGINT UNSIGNED NOT NULL,
    CONSTRAINT chk_branch_phone_range CHECK (BranchContact > 0 AND BranchContact <= 9999999999),
    CONSTRAINT chk_branch_pincode_length CHECK (Pincode >= 100000 AND Pincode <= 999999) -- Check pincode range
    -- CONSTRAINT fk_branch_manager
    -- FOREIGN KEY (ManagerID)
    -- REFERENCES Manager(ManagerID) -- Assuming Manager table exists
);

INSERT INTO Branch (StreetID, City, LandMark, State, Pincode, BranchContact) VALUES 
(116, 'Seattle', 'Downtown Seattle', 'Washington', 981201, 1234567890), 
(117, 'Miami', 'Downtown Miami', 'Florida', 331101, 9876543210), 
(118, 'Denver', 'Downtown Denver', 'Colorado', 807201, 9998887770), 
(119, 'Portland', 'Downtown Portland', 'Oregon', 937201, 7778889990), 
(120, 'Atlanta', 'Downtown Atlanta', 'Georgia', 303901, 1112223330),
(121, 'San Francisco', 'Downtown San Francisco', 'California', 941101, 5556667770),
(122, 'Boston', 'Downtown Boston', 'Massachusetts', 120101, 6667778880),
(123, 'Las Vegas', 'The Strip', 'Nevada', 891101, 7778889990),
(124, 'Seattle', 'Pike Place Market', 'Washington', 986104, 8889990000),
(125, 'Chicago', 'Navy Pier', 'Illinois', 606211, 9990001110),
(126, 'New Orleans', 'French Quarter', 'Louisiana', 701512, 3334445550),
(127, 'Orlando', 'Walt Disney World', 'Florida', 322830, 4445556660),
(128, 'Denver', 'Red Rocks Amphitheatre', 'Colorado', 805465, 7779990000),
(129, 'San Francisco', 'Golden Gate Bridge', 'California', 941229, 8889991110),
(130, 'New York', 'Times Square', 'New York', 100036, 9990001110);





CREATE TABLE Manager (
    ManagerID INT PRIMARY KEY NOT NULL auto_increment,
    FirstName VARCHAR(50) NOT NULL,
    MiddleName VARCHAR(50),
    LastName VARCHAR(50) NOT NULL,
    ManagerContact VARCHAR(20) NOT NULL,
    ManagerEmail VARCHAR(100) NOT NULL,
    BranchID INT NOT NULL,
    CONSTRAINT fk_manager_branch
    FOREIGN KEY (BranchID)
    REFERENCES Branch(BranchID) ON DELETE CASCADE -- Assuming Branch table exists
);

INSERT INTO Manager (FirstName, MiddleName, LastName, ManagerContact, ManagerEmail, BranchID) VALUES
('John', NULL, 'Doe', '123-456-7890', 'john.doe@example.com', 1),
('Jane', 'A', 'Smith', '987-654-3210', 'jane.smith@example.com', 2),
('Michael', 'B', 'Johnson', '999-888-7770', 'michael.johnson@example.com', 3),
('Emily', 'C', 'Brown', '777-888-9990', 'emily.brown@example.com', 4),
('David', 'D', 'Wilson', '111-222-3330', 'david.wilson@example.com', 5),
('Sarah', NULL, 'Taylor', '555-666-7770', 'sarah.taylor@example.com', 6),
('Christopher', 'E', 'Anderson', '666-777-8880', 'christopher.anderson@example.com', 7),
('Jessica', 'F', 'Martinez', '777-888-9990', 'jessica.martinez@example.com',8),
('Matthew', 'G', 'Hernandez', '888-999-0000', 'matthew.hernandez@example.com', 9),
('Andrew', 'H', 'Young', '999-000-1110', 'andrew.young@example.com', 10),
('Elizabeth', NULL, 'Lee', '333-444-5550', 'elizabeth.lee@example.com', 11),
('Daniel', 'I', 'Gonzalez', '444-555-6660', 'daniel.gonzalez@example.com', 12),
('Jennifer', 'J', 'Perez', '777-999-0000', 'jennifer.perez@example.com', 13),
('James', 'K', 'Robinson', '888-999-1110', 'james.robinson@example.com', 14),
('Olivia', 'L', 'Walker', '999-000-1110', 'olivia.walker@example.com', 15);



CREATE TABLE Employee (
    EmployeeID INT PRIMARY KEY NOT NULL auto_increment,
    FirstName VARCHAR(50) NOT NULL,
    MiddleName VARCHAR(50),
    LastName VARCHAR(50) NOT NULL,
    ManagerID INT NOT NULL,
    EmployeeContact BIGINT UNSIGNED NOT NULL,
    EmployeeEmail VARCHAR(100) NOT NULL,
    JoiningDate DATE NOT NULL,
    Position_ VARCHAR(100) NOT NULL,
    
    FOREIGN KEY (ManagerID) REFERENCES Manager(ManagerID), -- Assuming Manager table exists

    CONSTRAINT chk_employee_contact_range CHECK (EmployeeContact BETWEEN 1000000000 AND 9999999999), -- Check range of EmployeeContact
    
    CONSTRAINT chk_employee_email CHECK (EmployeeEmail LIKE '%@%') -- Check that email contains '@'
);

INSERT INTO Employee (FirstName, MiddleName, LastName, ManagerID, EmployeeContact, EmployeeEmail, JoiningDate, Position_) 
VALUES 
('John', NULL, 'Doe', 1, 1234567890, 'john.doe@example.com', '2024-01-15', 'Sales Associate'),
('Alice', 'A', 'Smith', 2, 2345678901, 'alice.smith@example.com', '2024-02-16', 'Customer Service Representative'),
('Michael', 'B', 'Johnson', 3, 3456789012, 'michael.johnson@example.com', '2024-03-17', 'Store Manager'),
('Emily', 'C', 'Brown', 4, 4567890123, 'emily.brown@example.com', '2024-04-18', 'Assistant Manager'),
('David', 'D', 'Wilson', 5, 5678901234, 'david.wilson@example.com', '2024-05-19', 'Sales Associate'),
('Sarah', NULL, 'Taylor', 6, 6789012345, 'sarah.taylor@example.com', '2024-06-20', 'Customer Service Representative'),
('Christopher', 'E', 'Anderson', 7, 7890123456, 'christopher.anderson@example.com', '2024-07-21', 'Store Manager'),
('Jessica', 'F', 'Martinez', 8, 8901234567, 'jessica.martinez@example.com', '2024-08-22', 'Assistant Manager'),
('Matthew', 'G', 'Hernandez', 9, 9012345678, 'matthew.hernandez@example.com', '2024-09-23', 'Sales Associate'),
('Andrew', 'H', 'Young', 10, 1234567890, 'andrew.young@example.com', '2024-10-24', 'Customer Service Representative'),
('Elizabeth', NULL, 'Lee', 11, 2345678901, 'elizabeth.lee@example.com', '2024-11-25', 'Store Manager'),
('Daniel', 'I', 'Gonzalez', 12, 3456789012, 'daniel.gonzalez@example.com', '2024-12-26', 'Assistant Manager'),
('Jennifer', 'J', 'Perez', 13, 4567890123, 'jennifer.perez@example.com', '2025-01-27', 'Sales Associate'),
('James', 'K', 'Robinson', 14, 5678901234, 'james.robinson@example.com', '2025-02-28', 'Customer Service Representative'),
('Olivia', 'L', 'Walker', 15, 6789012345, 'olivia.walker@example.com', '2025-03-29', 'Store Manager');


CREATE TABLE orderids(
	EmployeeID INT  NOT NULL,
    orderids INT NOT NULL,
    FOREIGN KEY (EmployeeID)
    REFERENCES Employee(EmployeeID)
    
);

INSERT INTO orderids (EmployeeID, orderids) VALUES 
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10),
(11, 11),
(12, 12),
(13, 13),
(14, 14),
(15, 15);


CREATE TABLE productids(
	EmployeeID INT  NOT NULL,
    productids INT NOT NULL,
    FOREIGN KEY (EmployeeID)
    REFERENCES Employee(EmployeeID)
);

INSERT INTO productids (EmployeeID, productids) VALUES 
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10),
(11, 11),
(12, 12),
(13, 13),
(14, 14),
(15, 15);

CREATE TABLE LoginAttempts (
    email VARCHAR(255) NOT NULL,
    attempts INT NOT NULL DEFAULT 0,
    last_attempt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (email)
);

CREATE TABLE LockedUsers (
    email VARCHAR(255) NOT NULL,
    locked_until TIMESTAMP,
    PRIMARY KEY (email)
);


DELIMITER //

CREATE TRIGGER After_Login_Attempt
AFTER INSERT ON LoginAttempts
FOR EACH ROW
BEGIN
    DECLARE attempt_count INT;
    SELECT attempts INTO attempt_count FROM LoginAttempts WHERE email = NEW.email;

    IF attempt_count >= 3 THEN
        UPDATE LockedUsers SET locked_until = ADDTIME(NOW(), '0 0:1:0') WHERE email = NEW.email;
    END IF;
END;
//

CREATE TRIGGER Before_Login
BEFORE INSERT ON LoginAttempts
FOR EACH ROW
BEGIN
    DECLARE locked_until_time TIMESTAMP;
    SELECT locked_until INTO locked_until_time FROM LockedUsers WHERE email = NEW.email;

    IF locked_until_time > NOW() THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'User is locked. Try again later.';
    END IF;
END;
//

DELIMITER ;

CREATE TABLE InsufficientBalanceAttempts (
    attempt_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    attempt_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER //

CREATE TRIGGER Insufficient_Balance_Trigger
AFTER INSERT ON InsufficientBalanceAttempts
FOR EACH ROW
BEGIN
    DECLARE attempt_count INT;
    DECLARE email_var VARCHAR(255);
    
    -- Retrieve the email of the user making the attempt
    SELECT email INTO email_var FROM InsufficientBalanceAttempts WHERE attempt_id = NEW.attempt_id;
    
    -- Count the number of insufficient balance attempts for the user
    SELECT COUNT(*) INTO attempt_count FROM InsufficientBalanceAttempts WHERE email = email_var;
    
    -- If attempts exceed 3, lock the user out for 30 seconds
    IF attempt_count > 3 THEN
        UPDATE LockedUsers SET locked_until = ADDTIME(NOW(), '0 0:0:30') WHERE email = email_var;
    END IF;
END;
//

DELIMITER ;