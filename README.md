# AI-Health-System

Here is the finalized GitHub repository description, customized specifically for your Python, Streamlit, MySQL, and OpenRouter API stack.
You can copy and paste this directly into your repository's README.md file.
------------------------------
## AI-Powered Health Prediction Dashboard
A secure, data-driven web application built with Python and Streamlit to manage patient health records and predict health risks. The system integrates a persistent MySQL database with the OpenRouter API to analyze blood test results and automatically generate clinical risk remarks.
## 🚀 Key Features

* Complete CRUD Operations: Create, Read, Update, and Delete patient diagnostic profiles seamlessly from a centralized Streamlit dashboard.
* OpenRouter AI Integration: Dynamically pipes validated blood metrics (Glucose, Haemoglobin, Cholesterol) to OpenRouter models to evaluate health risks.
* Strict Data Validation: Built-in safeguards to catch formatting issues, prevent future dates of birth, and ensure blood metrics are strictly numeric.
* Relational Storage: Backed by a MySQL Server to guarantee reliable, long-term data persistence and structured data management.
* Clean Analytics UI: Responsive, side-by-side layout utilizing Streamlit elements for quick diagnostic data entry and clear reporting.

## 📊 Patient Data Fields Tracked

* Full Name
* Date of Birth (Validated: past dates only)
* Email Address (Validated format)
* Glucose Levels (Numeric, mg/dL)
* Haemoglobin Levels (Numeric, g/dL)
* Cholesterol Levels (Numeric, mg/dL)
* Remarks (Automated clinical insights generated via OpenRouter API)

## 🛠️ Tech Stack

* Frontend & UI: Streamlit (Python-based interactive dashboard framework)
* Backend Logic: Python 3.x
* Database: MySQL Server
* AI/ML API Integration: OpenRouter API (utilizing advanced language/reasoning models)

## 🔧 Installation & Setup## 1. Prerequisites
Ensure you have MySQL Server running locally or hosted externally, and a Python 3.8+ environment.
## 2. Clone and Prepare the Project

git clone https://github.com
cd your-repo-name

## 3. Configure Secrets (.env)
Create a .env file in the root directory to store your private credentials. Do not commit this file to GitHub.

OPENROUTER_API_KEY=your_openrouter_api_key_here
DB_HOST=localhost
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_NAME=health_prediction_db

## 4. Install Dependencies

pip install -r requirements.txt

## 5. Run the Application
Initialize the Streamlit server locally:

streamlit run app.py

