from flask import Flask, render_template, request, jsonify
import sqlite3
from chat import get_response

app = Flask(__name__)


# Function to initialize the database
def init_db():
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY,
            user_input TEXT,
            bot_response TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database
init_db()


@app.get("/")
def index_get():
    return render_template("base.html")

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

@app.route("/Suggestion")
def tips():
    return render_template("tips.html")

# Route to handle user input and get bot response
@app.route("/predict", methods=["POST"])
def predict():
    # Get user input from request
    text = request.json.get("message")

    # Get bot response
    response = get_response(text)

    # Store user input and bot response in the database
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO conversations (user_input, bot_response) VALUES (?, ?)', (text, response))
    conn.commit()
    conn.close()

    # Prepare response message
    message = {"answer": response}
    return jsonify(message)

# Function to retrieve conversations from the database
def get_conversations():
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM conversations')
    conversations = cursor.fetchall()
    conn.close()
    return conversations

# Route to display conversations
@app.route("/conversations")
def display_conversations():
    conversations = get_conversations()
    return render_template("convo.html", conversations=conversations)


if __name__ == "__main__":
    app.run(debug=True)
