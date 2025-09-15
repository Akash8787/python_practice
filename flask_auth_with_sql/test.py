from flask import Flask, render_template, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
import bcrypt
import pyodbc
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# -------------------------------------------
# Database Connection
# -------------------------------------------
driver = 'ODBC Driver 17 for SQL Server'
server = 'SIPL147\\SQLEXPRESS'
database = 'db_test'

try:
    conn = pyodbc.connect(
        f'DRIVER={{{driver}}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    print("✅ Successfully connected to SQL Server!")
except pyodbc.Error as e:
    print(f"❌ Connection failed: {e}")
    exit()

# -------------------------------------------
# Login Required Decorator
# -------------------------------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("You must be logged in to view this page.")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# -------------------------------------------
# Forms
# -------------------------------------------
class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_email(self, email):
        cursor.execute("SELECT email FROM users WHERE email = ?", (email.data,))
        user = cursor.fetchone()
        if user:
            raise ValidationError("This email is already registered. Please use a different email.")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

# -------------------------------------------
# Routes
# -------------------------------------------
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, hashed_password))
            conn.commit()
            flash("Registration successful. Please login.")
            return redirect(url_for('login'))
        except pyodbc.Error as e:
            print(f"Database error: {e}")
            conn.rollback()
            flash("Something went wrong. Try again.")
    return render_template("register.html", form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[3]):
            session['user_id'] = user[0]
            flash("Login successful.")
            return redirect(url_for('dashboard'))
        else:
            flash("Login failed. Please check your email and password.")
            return redirect(url_for('login'))

    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()
    cursor.close()

    if user:
        return render_template('dashboard.html', user=user)
    flash("User not found.")
    return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    flash("You have been logged out.")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)