## Presentation
This project is developped by following this tutorial:
https://flask.palletsprojects.com/en/1.1.x/tutorial/

### 1. Application setup
Instead of creating a Flask instance globally, we'll create it inside the application function: any configuration, registration, and other setup the application needs will happen inside the function, then the application will be returned.

The __init__.py inside flaskr directory serves double duty: it will contain the application factory, and it tells Python that the flaskr directory should be treated as a package.

We can run the application like this:
```
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```
Then we can visit http://localhost:5000/hello

### 2. Define and Access the Database
We use MySQL database to store users and posts. We won't play directly with SQL. We'll use ORM to interact with database, so we can treat data as Python object. SQLAlchemy is database framwork, it offres ORM and basic database manipulation.
```
pip install flask-sqlalchemy
```

first step: create database in mysql
```
mysql -u root -p
create database flaskr
```

second step: create tables in database
```
python manager.py db init
python manager.py db migrate
python manager.py db upgrade
```

third step: run the application
```
python manager.py runserver
```

### 3. Blueprint and Views
A view function is the code you write to respond to requests to your application. Flask uses patterns to match the incoming request URL to the view that should handle it.
A Blueprint is a way to organize a group of related views and other code.

g is a special object that is unique for each request. It is used to store data that might be accessed by multiple functions during the request.

The url_for() function generates the URL to a view based on a name and arguments. The name associated with a view is also called the endpoint, by default it’s the same as the name of the view function.

### 4. Templates
Templates are files that contain static data as well as placeholders for dynamic data.
A template is rendered with specific data to produce a final document.
Flask uses the Jinja template library to render templates.

In Flask, Jinja is configured to autoescape any data that is rendered in HTML templates. This means that it’s safe to render user input; any characters they’ve entered that could mess with the HTML, such as < and > will be escaped with safe values that look the same in the browser but don’t cause unwanted effects.

#### Jinja syntax:
Anything between {{ and }} is an expression that will be output to the final document.
{% and %} denotes a control flow statement like if and for.
loop.last is a special variable available inside Jinja for loops.

g is automatically available in templates.
url_for() is also automatically available, and is used to generate URLs to views instead of writing them out manually.
request is another variable that’s automatically available in templates.

get_flashed_messages(): you used flash() in the views to show error messages, and this is the code that will display them.

#### base template
There are three blocks defined here that will be overridden in the other templates:
- {% block title %} will change the title displayed in the browser’s tab and window title.
- {% block header %} is similar to title but will change the title displayed on the page.
- {% block content %} is where the content of each page goes, such as the login form or a blog post.

#### auth register.html
The input tags are using the required attribute. This tells the browser not to submit the form until those fields are filled in. If the user is using an older browser that doesn’t support that attribute, or if they are using something besides a browser to make requests, you still want to validate the data in the Flask view. It’s important to always fully validate the data on the server, even if the client does some validation as well.

### 5. Static Files
Some CSS can be added to add style to the HTML layout you constructed. The style won’t change, so it’s a static file rather than a template.

Tuto CSS: https://developer.mozilla.org/fr/docs/Web/CSS

### 6. Make the project installable
Making your project installable means that you can build a distribution file and install that in another environment, just like you installed Flask in your project’s environment.

The setup.py file describes your project and the files that belong to it.
- packages tells Python what package directories (and the Python files they contain) to include. find_packages() finds these directories automatically so you don’t have to type them out.
- To include other files, such as the static and templates directories, include_package_data is set. Python needs another file named MANIFEST.in to tell what this other data is.

After editing setup.py and MANIFEST.in, we can install the project in virtual environment:
```
pip install -e .
```
Now you can run the project from anywhere, not just inside the flask-tuto directory.

### 7. Test Coverage
To test and measure the code, we need to install:
```
pip install pytest coverage
```
The tests/conftest.py file contains setup functions called fixtures that each test will use.
Pytest uses fixtures by matching their function names with the names of arguments in the test functions. For example, the test_hello function takes a client argument. Pytest matches that with the client fixture function, calls it, and passes the returned value to the test function.

client.get() makes a GET request and returns the Response object returned by Flask.
Similarly, client.post() makes a POST request, converting the data dict into form data.

data contains the body of the response as bytes. If you expect a certain value to render on the page, check that it’s in data.

pytest.mark.parametrize tells Pytest to run the same test function with different arguments.

Using client in a with block allows accessing context variables such as session after the response is returned.

#### running the tests
To run the tests, use the pytest command. It will find and run all the test functions you’ve written.
```
pytest
pytest -v # get a list of each test function rather than dots.
```

To measure the code coverage of your tests, use the coverage to run pytest instead of running it directly.
```
coverage run -m pytest
```
You can either view a simple coverage report in the terminal:
```
coverage report
```
An HTML report allows you to see which lines were covered in each file:
```
coverage html
```

### 8. Deploy to production
When you want to deploy your application elsewhere, you build a distribution file. The current standard for Python distribution is the wheel format, with the .whl extension.
Running setup.py with Python gives you a command line tool to issue build-related commands. The bdist_wheel command will build a wheel distribution file.
```
pip install wheel
python setup.py bdist_wheel
```
Then you can try to install the flaskr-1.0.0-py3-none-any.whl in another machine. We can set up a new virtualenv to test it:
```
cd flask-tuto
python3 -m venv venv # this will create a venv directory
venv\Scripts\activate # on Windows, activate the environment
```
Within the activated environment, install the application and dependencies:
```
pip install flaskr-1.0.0-py3-none-any.whl
pip install flask-sqlalchemy
pip install mysqlclient
set FLASK_APP=flaskr
flask run
```
#### Run with a production server
flask run uses the built-in development server Werkzeug for convenience,
in production env, we need to use procuction WSGI server, such as Waitress:
```
pip install waitress
waitress-serve --call flaskr:create_app
```

#### Configure the secret key
default value for SECRET_KET is 'dev', we can generate a random secret key for procuction:
```
python -c 'import os; print(os.urandom(16))'
```
