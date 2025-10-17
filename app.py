from flask import Flask, render_template
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

@app.route('/')
def home():
    """Home page route"""
    return render_template('index.html')

@app.route('/about')
def about():
    """About page route"""
    return render_template('about.html')

if __name__ == '__main__':
    # Debug mode is only for development - disable in production
    app.run(debug=True, host='127.0.0.1')
