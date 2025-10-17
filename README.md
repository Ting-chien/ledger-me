# ledger-me
LedgerMe is a Web App to track my income/expense, investment and any financial activities 😎

## Features
- Track income and expenses
- Manage investment portfolios
- Visualize financial data
- Generate financial reports

## Technologies
- Python 3.x
- Flask 3.0.0
- HTML/CSS/JavaScript

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Ting-chien/ledger-me.git
cd ledger-me
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables (optional):
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Running the Application

Run the Flask development server:
```bash
python app.py
```

Or using Flask's built-in command:
```bash
flask run
```

The application will be available at `http://localhost:5000`

## Project Structure
```
ledger-me/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment variables
├── templates/          # HTML templates
│   ├── base.html      # Base template
│   ├── index.html     # Home page
│   └── about.html     # About page
└── static/            # Static files
    ├── css/
    │   └── style.css  # Stylesheets
    └── js/
        └── main.js    # JavaScript files
```

## License
MIT
