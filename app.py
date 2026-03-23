# Name: Logan Miranowski
# Class: INF360
# Project: Flask Web App

from flask import Flask, render_template

app = Flask(__name__)

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    print("Starting the Flask app...")
    app.run(debug=True)