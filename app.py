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


if __name__ == "__main__":
    app.run(debug=True)
