# pelago

This is a repo for Pelago assessment test

### High Level Design

![](images/High-Level-Design.png)

1. UI/UX layer
   - Channels to interact with server. Supports any UI channels like Mobile App, Web App, PostMan rest cleint etc
2. Middleware Layer
   - This is the application server and business logic process in this layer
3. Data Storage Layer
   - Data will be stored in this layer
4. Offline Process
   - Any backend process to update data from admin.

### Setting up virtual environment

It is always better to use virtual environment to switch between Python versions.

```
pip3 install virtualenv
```

```
python -m venv .venv
source .venv/bin/activate
```

### Running Application Server

### Offline process to add/insert package details to the databas

### Running test cases

Execute below command from src folder to run unit test cases

```
python3 -m unittest test_*.py
```

Execute below command from src folder to see code coverage

```
coverage run -m unittest test_*.py

# to see report in the console
coverage report

# To show code coverate in web page
coverage html
```
