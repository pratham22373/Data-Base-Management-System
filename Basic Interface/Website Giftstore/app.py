from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, text
# from database import engine
from sqlalchemy import create_engine, text

engine = create_engine("mysql+pymysql://root:pmroot@localhost/GIFTSTOREAPP?charset=utf8mb4")
app = Flask(__name__)

# Set a secret key for the Flask application
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

failed_login_attempts = {}
failed_login_attempts_vendor = {}
failed_login_attempts_admin = {}


@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/info')
def info():
    user_type = request.args.get('user_type') 
    return render_template('index.html', user_type=user_type)


@app.route('/info/login/customer', methods=['GET', 'POST'])
def login_customer():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
      
        with engine.connect() as connection:
            query = text("SELECT * FROM person WHERE email = :email AND password_ = :password")
            result = connection.execute(query, {'email': email, 'password': password})
            user = result.fetchone()
        if user:
            failed_login_attempts.pop(email, None)
            return redirect(url_for('mainmenu', person_id=user[0]))
            
        else:
            failed_login_attempts[email] = failed_login_attempts.get(email, 0) + 1
            
            if failed_login_attempts[email] >= 3:
                
                return redirect(url_for('hello_world'))
            else:
                flash('Invalid email or password for customer', 'error')  
            return render_template('login_customer.html')
    else:
        return render_template('login_customer.html')



# Login route for vendors
@app.route('/info/login/vendor', methods=['GET', 'POST'])
def login_vendor():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Check credentials in the vendor table
        with engine.connect() as connection:
            query = text("SELECT * FROM person WHERE email = :email AND password_ = :password")
            result = connection.execute(query, {'email': email, 'password': password})
            user = result.fetchone()
        if user:
            # Vendor authentication successful
            failed_login_attempts_vendor.pop(email, None)
            return redirect(url_for('vendor_dashboard'))
        else:
            failed_login_attempts_vendor[email] = failed_login_attempts_vendor.get(email, 0) + 1
            
            if failed_login_attempts_vendor[email] >= 3:
                
                return redirect(url_for('hello_world'))
            else:
                flash('Invalid email or password for vendor', 'error')  # Flash error message
            return render_template('login_vendor.html')
    else:
        return render_template('login_vendor.html')
    
# Login route for admins -----------------------------------------------------------------changes required in admin
@app.route('/info/login/admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Check credentials in the admin table
        with engine.connect() as connection:
            query = text("SELECT * FROM Manager WHERE email = :email AND password = :password")
            result = connection.execute(query, email=email, password=password)
            user = result.fetchone()
        if user:
            # Admin authentication successful
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid email or password for admin', 'error')  # Flash error message
            return render_template('login_admin.html')
    else:
        return render_template('login_admin.html')




@app.route('/info/login/customer/mainmenu')
def mainmenu():
    person_id = request.args.get('person_id')
    
    return render_template('mainmenu.html')




@app.route('/info/signup/customer', methods=['GET', 'POST'])
def signup_customer():
    if request.method == 'POST':
        # Extract form data
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        phone_no = request.form['phone_no']
        email = request.form['email']
        street_id = request.form['street_id']
        city = request.form['city']
        landmark = request.form['landmark']
        states = request.form['states']
        pincode = request.form['pincode']
        dob = request.form['dob']
        password = request.form['password']
        
        # Validate data against constraints
        if not first_name:
            flash('First name is required.', 'error')
            return render_template('signup_customer.html')
        if not last_name:
            flash('Last name is required.', 'error')
            return render_template('signup_customer.html')
        if not phone_no.isdigit() or len(phone_no) != 10:
            flash('Invalid phone number.', 'error')
            return render_template('signup_customer.html')
        if '@' not in email or '.' not in email.split('@')[-1]:
            flash('Invalid email format.', 'error')
            return render_template('signup_customer.html')
        if not street_id:
            flash('Street ID is required.', 'error')
            return render_template('signup_customer.html')
        if not city:
            flash('City is required.', 'error')
            return render_template('signup_customer.html')
        if not landmark:
            flash('Landmark is required.', 'error')
            return render_template('signup_customer.html')
        if not states:
            flash('State is required.', 'error')
            return render_template('signup_customer.html')
        if not pincode.isdigit() or len(pincode) != 6:
            flash('Invalid pincode.', 'error')
            return render_template('signup_customer.html')
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('signup_customer.html')
        
        # Add customer to the database (insert into person table)
        with engine.connect() as connection:
            query = text("""
            INSERT INTO person 
                (first_name, middle_name, last_name, phone_no, email, street_id, city, landmark, states, pincode, dob, password_) 
            VALUES 
                (:first_name, :middle_name, :last_name, :phone_no, :email, :street_id, :city, :landmark, :states, :pincode, :dob, :password)
            """)
            connection.execute(query, {
                'first_name': first_name,
                'middle_name': middle_name,
                'last_name': last_name,
                'phone_no': phone_no,
                'email': email,
                'street_id': street_id,
                'city': city,
                'landmark': landmark,
                'states': states,
                'pincode': pincode,
                'dob': dob,
                'password': password
            })
            connection.commit()
        return redirect(url_for('mainmenu'))
    else:
        return render_template('signup_customer.html')


@app.route('/info/signup/vendor', methods=['GET', 'POST'])
def signup_vendor():
    if request.method == 'POST':
        # Extract form data
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        phone_no = request.form['phone_no']
        email = request.form['email']
        street_id = request.form['street_id']
        city = request.form['city']
        landmark = request.form['landmark']
        states = request.form['states']
        pincode = request.form['pincode']
        dob = request.form['dob']
        password = request.form['password']
        
        # Validate data against constraints
        if not first_name:
            flash('First name is required.', 'error')
            return render_template('signup_vendor.html')
        if not last_name:
            flash('Last name is required.', 'error')
            return render_template('signup_vendor.html')
        if not phone_no.isdigit() or len(phone_no) != 10:
            flash('Invalid phone number.', 'error')
            return render_template('signup_vendor.html')
        if '@' not in email or '.' not in email.split('@')[-1]:
            flash('Invalid email format.', 'error')
            return render_template('signup_vendor.html')
        if not street_id:
            flash('Street ID is required.', 'error')
            return render_template('signup_vendor.html')
        if not city:
            flash('City is required.', 'error')
            return render_template('signup_vendor.html')
        if not landmark:
            flash('Landmark is required.', 'error')
            return render_template('signup_vendor.html')
        if not states:
            flash('State is required.', 'error')
            return render_template('signup_vendor.html')
        if not pincode.isdigit() or len(pincode) != 6:
            flash('Invalid pincode.', 'error')
            return render_template('signup_vendor.html')
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('signup_vendor.html')
        
        # Add customer to the database (insert into person table)
        with engine.connect() as connection:
            query = text("""
            INSERT INTO person 
                (first_name, middle_name, last_name, phone_no, email, street_id, city, landmark, states, pincode, dob, password_) 
            VALUES 
                (:first_name, :middle_name, :last_name, :phone_no, :email, :street_id, :city, :landmark, :states, :pincode, :dob, :password)
            """)
            connection.execute(query, {
                'first_name': first_name,
                'middle_name': middle_name,
                'last_name': last_name,
                'phone_no': phone_no,
                'email': email,
                'street_id': street_id,
                'city': city,
                'landmark': landmark,
                'states': states,
                'pincode': pincode,
                'dob': dob,
                'password': password
            })
            connection.commit()
        return redirect(url_for('mainmenu'))
    else:
        return render_template('signup_vendor.html')

if __name__ == "__main__":
    app.run(debug=True)



# from flask import Flask

# app = Flask(__name__)

# @app.route('/')

# def home():
#     return "Hello World <h1> HEWFSDF </h1>"

# if __name__ == "__main__":
#     app.run()