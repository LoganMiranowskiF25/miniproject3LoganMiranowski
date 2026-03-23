# Name: Logan Miranowski
# Class: INF360
# Project: Flask Web App

from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "supersectretkey"

def init_db():
    conn = sqlite3.connect("app.db")
    c = conn.cursor()

    # Create users table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # Create posts table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()

init_db()

# Routes start here

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

#Route for dashboard
@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect("app.db")
    c = conn.cursor()
    # join posts with users to get the username for each post
    c.execute('''
        SELECT posts.title, posts.content, users.username 
        FROM posts
        JOIN users ON posts.user_id = users.id
        ORDER BY posts.id DESC
    ''')
    posts = c.fetchall()
    conn.close()

    return render_template('dashboard.html', posts=posts)

#Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            flash('Login successful!')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials.')

    return render_template('login.html')

#Route for registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match.')
            return render_template('register.html')
        
        try:
            conn = sqlite3.connect("app.db")
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            flash("Successfully registered! Please log in.")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Username already exists. Please choose a different one.")
            return render_template('register.html')

    return render_template('register.html')

#route for creating a new post
@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        #assume user_id is 1 for simplicity, in a real app you would get this from the session
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute("INSERT INTO posts (user_id, title, content) VALUES (?, ?, ?)", (1, title, content))
        conn.commit()
        conn.close()
        flash("Post created successfully!")
        return redirect(url_for('dashboard'))

    return render_template('form_page.html')

if __name__ == '__main__':
    print("Starting the Flask app...")
    app.run(debug=True)