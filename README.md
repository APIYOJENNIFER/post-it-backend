# post-it-backend

PostIt ​is a simple application that allows friends and colleagues to create groups for notifications. This way one person can post notifications to everyone by sending a message once. The application allows people to create accounts, create groups add registered users to the groups, and then send messages to these groups whenever they want.

# Project Setup

1. After cloning the repo, set up a virtual environment
   `python3 -m venv .venv`

2. Activate the virtual environment
   `. .venv/bin/activate`

3. Install the dependencies in requirements.txt
   `pip install -r requirements.txt`

4. Configure PostgresSQL
   i) Open the PostgresSQL command line interface
   `psql postgres`

   ii) From your terminal, create a database
   `CREATE DATABASE postit;`

   iii) Create a user, feel free to replace the username and password
   `CREATE USER admin WITH PASSWORD 'password';`

   iv) Modify the connection parameters for the created user
   `ALTER ROLE admin SET client_encoding TO 'utf8';`
   `ALTER ROLE admin SET default_transaction_isolation TO 'read committed';`
   `ALTER ROLE admin SET timezone TO 'UTC';`

   v) Grant the user access rights to the database
   `GRANT ALL PRIVILEGES ON DATABASE postit TO admin;`

   vi) Exit the postgres command line
   `\q`

5. Create a .env file at the root of the project and set the database configurations there
   `SECRET_KEY=your_secret_key`
   `DB_NAME=postit`
   `DB_USER=admin`
   `DB_PASSWORD=your_password`
   `DB_HOST=localhost`
   `DB_PORT=5432`

6. Make migrations
   `python manage.py makemigrations`

7. Migrate to create tables
   `python manage.py migrate`

8. Create a superuser
   `python manage.py createsuperuser`

9. Start the server
   `python manage.py runserver`
