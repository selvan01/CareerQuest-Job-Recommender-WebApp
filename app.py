from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from chat import get_response

app = Flask(__name__)
app.secret_key = '1234'

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# User model
class User(UserMixin):
    def __init__(self, id_, username):
        self.id = id_
        self.username = username

    @staticmethod
    def get(user_id):
        conn = sqlite3.connect('chatbot.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        if not user:
            return None
        return User(str(user["id"]), user["username"])

    @staticmethod
    def get_by_username(username):
        conn = sqlite3.connect('chatbot.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        if not user:
            return None
        return User(str(user["id"]), user["username"])

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


# Function to initialize the database
def init_db():
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            user_input TEXT,
            bot_response TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit()
    conn.close()

# Initialize the database
init_db()

@app.get("/")
def index_get():
    if current_user.is_authenticated:
        return render_template("base.html")
    else:
        return redirect(url_for('login'))

@app.route("/Contact")
def Contact():
    return render_template("contact.html")

@app.route("/tenth")
def tenth():
    return render_template("10th.html")

@app.route("/twelve")
def twelve():
    return render_template("12th.html")

@app.route("/College")
def College():
    return render_template("college.html")

@app.route("/Courses")
def Courses():
    return render_template("course.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('chatbot.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        if user and check_password_hash(user['password_hash'], password):
            user_obj = User(user['id'], user['username'])
            login_user(user_obj, remember=True)
            return redirect(url_for('index_get'))  # Redirect to the base.html page
        flash('Invalid username or password')
    return render_template('login.html', login=True)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        try:
            conn = sqlite3.connect('chatbot.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            flash('Registration successful. Please log in.')
        except sqlite3.IntegrityError:  # Assuming the username is unique
            flash('Username already exists!')
        finally:
            conn.close()
        return redirect(url_for('login'))
    return render_template('register.html', login=False)

# Route to handle user input and get bot response
@app.post("/predict")
@login_required
def predict():
    text = request.get_json().get("message")
    # Assuming get_response(text) is your chatbot's response function
    response = get_response(text)
    message = {"answer": response}

    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO conversations (user_id, user_input, bot_response) VALUES (?, ?, ?)", (current_user.id, text, response))
    conn.commit()
    conn.close()

    return jsonify(message)


# Function to retrieve conversations from the database
def get_conversations():
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM conversations WHERE user_id = ?", (current_user.id,))
    conversations = cursor.fetchall()
    conn.close()
    return conversations

# Route to display conversations
@app.route("/conversations")
@login_required
def display_conversations():
    conversations = get_conversations()
    return render_template("convo.html", conversations=conversations)

@app.route('/logout', methods=['POST'])  # Ensure that the method is POST
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
