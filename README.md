# articles_admin_panel
An Admin Panel for Storing &amp; Updating News Articles

# Setup Steps (Windows):
  •	Install Git on OS if required
    o	https://git-scm.com/downloads 
  •	Clone Git Repository from:
    o	https://github.com/PavlosP30/articles_admin_panel.git 
  •	Install Python on OS if required 
    o https://www.python.org/downloads/
  •	Install Flask
    o	pip install Flask
  •	Create an Environment
    o	py -m venv env
  •	Activate the Environment
    o	env\Scripts\activate
  •	Install Flask Modules
    o	flask_sqlalchemy
      	pip install flask-sqlalchemy
    o	passlib
      	pip install passlib
    o	marshmallow
      	pip install flask-marshmallow
      	pip install -U flask-sqlalchemy marshmallow-sqlalchemy

# How to Run Server:
  • Navigate to app directory
  •	py app.py
  •	Open browser at http://127.0.0.1:5000/
  
  Note: DB Tables are dropped on each run of the application for testing purposes

# How to use:
## Admin Panel:
Login Credentials:
•	email = admin@admin.com
•	password = "admin1234"

## APIS:
Get Articles: http://127.0.0.1:5000/articles
Get Authors: http://127.0.0.1:5000/authors
Get News Categories: http://127.0.0.1:5000/news_categories
