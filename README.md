# Recipe App

This is a Django-based web application for managing recipes. Users can create, view, and search for recipes based on ingredients. The application features a user-friendly admin interface for managing recipes.

## User Goals
- **Browse Recipes**: Users can browse through a list of recipes.
- **Search Recipes**: Users can search for recipes by name or ingredient.
- **View Recipe Details**: Users can click on a recipe to view its details, including ingredients, cooking time, and difficulty.
- **Visualize Data**: Users can visualize recipe data using bar charts, pie charts, and line charts.
- **Authentication**: Users can log in and log out to manage their sessions securely.

## Project dependencies
### Dependencies used in development
- Django (4.2.11)
- pillow (10.2.0)
- pandas (2.0.3)
- matplotlib (3.7.5)
- django-environ (0.11.2)
- numpy (1.24.4)
### Dependencies used in production
- gunicorn (21.2.0)
- dj-database-url (2.1.0)
- psycopg2-binary (2.8.6)
- whitenoise (6.6.0)
- Brotli (1.1.0)
- django-cloudinary-storage (0.3.0)

## Technical Requirements
- Works on Python 3.6+ installations and Django version 3.
- Handles exceptions or errors that arise during user input, for example, then displays user-friendly error messages.
- Connects to a PostgreSQL database hosted locally on the same system (an SQLite database is needed during the development of your application).
- Provides an easy-to-use interface, supported by simple forms of input and concise, easy-to-follow instructions. Menus containing features like login and logout must be presented neatly—with concise and easy-to-follow prompts.
- Code with proper documentation and automated tests is uploaded on GitHub. A “requirements.txt” file is provided, containing the requisite modules for the project.


## Set up this App
1. Clone this repository.
2. Navigate to the recipe-app folder and run make install-dev
3. Setup Database by configuring DATABASES in the settings folder in dev.py for development.
4. Run migrations with make dev-migrate
5. Create a superuser by running make dev-superuser
6. Run make dev-start to check out the app in your browser under http://127.0.0.1:8000
