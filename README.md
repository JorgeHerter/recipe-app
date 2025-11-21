<<<<<<< HEAD
A2 Recipe Application (A2_Recipe_App)

This project is a full-fledged web application developed using the Django framework. The primary goal of this application is to allow users to input, store, and search for cooking recipes based on their ingredients, cooking times, and descriptions.

This repository structure reflects the initial setup phase as per the instructions in Achievement 2, Exercise 2.2.

🚀 Getting Started

Follow these steps to set up and run the application on your local machine.

1. Prerequisites

I have installed and verified Python on my system.

2. Virtual Environment Setup

It is best practice to use a virtual environment to manage project dependencies.

# Navigate into the project folder (A2_Recipe_App)
cd A2_Recipe_App

# Create the virtual environment named a2-ve-recipeapp
python -m venv a2-ve-recipeapp

# Activate the virtual environment
# On Windows:
.\a2-ve-recipeapp\Scripts\activate
# On macOS/Linux:
source a2-ve-recipeapp/bin/activate


3. Install Dependencies

With the virtual environment activated, install the required framework:

pip install django


4. Project Structure

The core Django project files are contained within the src directory, which was initially named recipe_project.

A2_Recipe_App/
├── a2-ve-recipeapp/      # Python Virtual Environment
└── src/                  # Django Project Root (formerly 'recipe_project')
    ├── manage.py         # Django's command-line utility
    └── src/              # Project settings and URL configurations (inner folder)
        ├── settings.py
        ├── urls.py
        └── ...


5. Running the Application

Navigate to the directory containing manage.py and execute the following commands.

A. Apply Migrations

Django includes default database structure for user authentication and the admin site. Run migrations to create these tables.

cd src
python manage.py migrate


B. Create Superuser (Admin Account)

To access the administrative dashboard, you must create a superuser.

python manage.py createsuperuser
# Follow the prompts to set username, email, and password.


C. Start the Development Server

Start the application server:

python manage.py runserver


You should see output similar to:

Starting development server at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
Quit the server with CTRL-BREAK.


6. Accessing the App

View the Default Page: Open your web browser and go to http://127.0.0.1:8000/.

Access the Admin Dashboard: Go to http://127.0.0.1:8000/admin/ and log in using the superuser credentials you created. This is where you will register and manage your Recipe models.

🛠 Tech Stack

Backend Framework: Django (Python)

Database: SQLite (default for development)
=======
# recipe-app
>>>>>>> 12380658ec9380aed6b81037d30390df3cb038af
