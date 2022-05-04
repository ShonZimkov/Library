# imports
import atexit
from datetime import date, timedelta
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import base
from modules import customers,books,loans
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from modules.login import User,LoginForm,RegisterForm
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config ['SECRET_KEY'] = 'shonpass'
bootstrap = Bootstrap(app)

# generate database schema
base.Base.metadata.create_all(base.engine)

# create a new session
session = base.Session()

# session for the job
session2 = base.Session2()

# login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Declaration of the task as a function
def print_date_time():
    all_loans=session2.query(loans.Loan).all()
    for loan in all_loans:
        if loan.status != 'Returned':
            return_date=loan.return_date
            today=date.today()
            if return_date < today:
                loan.status='Late Loan'
    session2.commit()
    session2.close()

@login_manager.user_loader
def load_user(user_id):
    user_id=session.query(User).filter(User.id==user_id).first()
    session.close()
    return user_id

#login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    try:
        if form.validate_on_submit():
            user = session.query(User).filter_by(username=form.username.data).first()
            if user:
                if check_password_hash(user.password, form.password.data):
                    login_user(user, remember=form.remember.data)
                    return redirect(url_for('dashboard'))
    except:
        flash('Invalid username or password')
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'
    session.close()
    return render_template('login.html', form=form)

#signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    try:
        if form.validate_on_submit():
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            session.add(new_user)
            session.commit()

            flash('New user has been created!Go login!')
            #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'
    except:
        flash('Username or Email are being used')
    session.close()
    return render_template('signup.html', form=form)

# after login home page
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

# logout option
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# home page
@app.route('/')
def home():
    return render_template('home.html')

# late loans page
@app.route('/late_loans')
@login_required
def late_loans():
    results = session.query(books.Book,loans.Loan,customers.Customer).select_from(books.Book).join(loans.Loan).join(customers.Customer).filter(loans.Loan.status=='Late Loan').all()
    session.close()
    return render_template('late_loans.html', results = results)

# show book page
@app.route('/books')
@login_required
def show_books():
    show_books = session.query(books.Book).all()
    session.close()
    return render_template('books.html', show_books = show_books)

# new book page
@app.route('/new_book',methods=["GET","POST"])
@login_required
def new_book():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['author'] or not request.form['year']:
           flash('Please enter all the fields', 'error')
        else:
            book = books.Book(request.form['name'], request.form['author'],
            request.form['year'], request.form['type'])
         
            session.add(book)
            session.commit()
            session.close()
            flash('Record was successfully added')
            return redirect(url_for('show_books'))
    return render_template('new_book.html')

# delete book page
@app.route('/delete_book', methods = ['GET', 'POST'])
@login_required
def delete_book():
    if request.method == 'POST':
        try:    
            if not request.form['name']:
                flash('Please enter all the fields', 'error')
            else:
                book = session.query(books.Book).filter(books.Book.name==request.form['name']).first()
                session.delete(book)
                session.commit()
                session.close()
        except:
            flash('No results')
            return redirect(url_for('show_books'))
    return render_template('delete_book.html')

# show customers page
@app.route('/customers')
@login_required
def show_customers():
    show_customers = session.query(customers.Customer).all()
    session.close()
    return render_template('customers.html', show_customers = show_customers)

#new customer page
@app.route('/new_customer', methods = ['GET', 'POST'])
@login_required
def new_customer():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['city'] or not request.form['age']:
           flash('Please enter all the fields', 'error')
        else:
            customer = customers.Customer(request.form['name'], request.form['city'],
            request.form['age'])
         
            session.add(customer)
            session.commit()
            session.close()
            flash('Record was successfully added')
            return redirect(url_for('show_customers'))
    return render_template('new_customer.html')

# delete customer page
@app.route('/delete_customer', methods = ['GET', 'POST'])
@login_required
def delete_customer():
    if request.method == 'POST':
        try:
            if not request.form['name']:
                flash('Please enter all the fields', 'error')
            else:
                customer = session.query(customers.Customer).filter(customers.Customer.name==request.form['name']).first()
                session.delete(customer)
                session.commit()
                session.close()
        except:
            flash('No results')
            return redirect(url_for('show_customers'))
    return render_template('delete_customer.html')

#show loans page
@app.route('/loans')
@login_required
def show_loans():
    results = session.query(books.Book,loans.Loan,customers.Customer).select_from(books.Book).join(loans.Loan).join(customers.Customer).all()
    session.close()
    return render_template('loans.html', results = results)

#new loan page
@app.route('/new_loan', methods = ['GET', 'POST'])
@login_required
def new_loan():

    if request.method == 'POST':
        if not request.form['book_id'] or not request.form['cust_id'] :
               flash('Please enter all the fields', 'error')
        else:
            loan = loans.Loan(request.form['book_id'],
                           request.form['cust_id'],
                           loan_date=date.today())
    
            session.add(loan)
            session.commit()
            results = session.query(books.Book,loans.Loan,customers.Customer).select_from(books.Book).join(loans.Loan).join(customers.Customer).filter(loans.Loan.id==loan.id).all()

            #join books and loans
            for book, loan , customer in results:
                book_type=book.type
                loan.loan_date = date.today()
                if int(book_type) == 1:
                    loan.return_date = loan.loan_date + timedelta(days=10)
                elif int(book_type) == 2:
                    loan.return_date= loan.loan_date + timedelta(days=5)
                elif int(book_type) == 3:
                    loan.return_date = loan.loan_date + timedelta(days=2)
            session.commit()
            session.close()
            flash('Record was successfully added')
            return redirect(url_for('show_loans'))
    return render_template('new_loan.html')

#return loan page
@app.route('/return_loan', methods = ['GET', 'POST'])
@login_required
def return_loan():
    if request.method == 'POST':
        if not request.form['book_id'] or not request.form['cust_id'] :
               flash('Please enter all the fields', 'error')
        else:
            loan = session.query(loans.Loan).filter(loans.Loan.cust_id==request.form['cust_id'],loans.Loan.book_id==request.form['book_id'],loans.Loan.status!='Late Loan').first()
            loan.status='Returned'
            session.commit()
            if loan ==[]:flash('No results')
            return redirect(url_for('show_loans'))
        session.close()
    return render_template('return_loan.html')

#delete a loan (optional for admin)
@app.route('/delete_loan', methods = ['GET', 'POST'])
@login_required
def delete_loan():
    if request.method == 'POST':
        try:
            if not request.form['id']:
                flash('Please enter all the fields', 'error')
            else:
                loan = session.query(loans.Loan).filter(loans.Loan.id==request.form['id']).first()
                session.delete(loan)
                session.commit()
        except:
            flash('No results')
            return redirect(url_for('show_loans'))
        session.close()
    return render_template('delete_loan.html')

# search book page
@app.route('/search_book', methods = ['GET', 'POST'])
@login_required
def search_book():
    if request.method == 'POST':
        if not request.form['name']:
               flash('Please enter all the fields', 'error')
        else:
            res = session.query(books.Book).filter(books.Book.name==request.form['name']).all()
            session.close()
            if res ==[]:flash('No results')
            return render_template('search_book.html',res=res)
    return render_template('search_book.html')

#search customer page
@app.route('/search_customer', methods = ['GET', 'POST'])
@login_required
def search_customer():
    if request.method == 'POST':
        if not request.form['name']:
               flash('Please enter all the fields', 'error')
        else:
            res = session.query(customers.Customer).filter(customers.Customer.name==request.form['name']).all()
            session.close()
            if res ==[]:flash('No results')
            return render_template('search_customer.html',res=res)
    return render_template('search_customer.html')


# run app and job
if __name__ == '__main__':      
    # Create the background scheduler
    scheduler = BackgroundScheduler()
    # Create the job
    scheduler.add_job(func=print_date_time, trigger="interval", hours=24)
    # Start the scheduler
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
    app.run(debug = True)
