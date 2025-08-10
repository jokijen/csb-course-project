# CSB-course-project

This project has been created for learning purposes for the course "Cyber Security Base: Project I" (University of Helsinki). The objective is to create a web application with five flaws from the OWASP top 10 -list, and provide fixes for them. The fixes are commented out from the code.

The OWASP top 10 can be found at https://owasp.org/Top10/


## Table of contents
- [Running the application](#running-the-application)
- [Credits](#credits)


## Running the application

Take the following steps to run the application, but be mindful that the app is not secure in its current state: 

1. Clone the repository to a location of your choice and go to its root directory
2. Create a file .env into the root directory and add a secret key:
```
SECRET_KEY=<your-secret-key>
DEBUG=<bool-value>
``` 
3. Create a virtual environment: $ python3 -m venv venv
4. Activate the virtual environment: $ source venv/bin/activate
5. Install necessary packages using pip: $ pip install -r requirements.txt
6. Run migrations: $ python manage.py migrate
7. Run the application: $ python manage.py runserver
8. Open a browser and navigate to 'http://localhost:8000/'
9. Add new users, login, and send messages


## Credits

- .gitignore template for Python by GitHub (edited by author): https://github.com/github/gitignore/blob/main/Python.gitignore