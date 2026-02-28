import requests

def dvwa_login():
    session = requests.Session()
    login_url = "http://localhost/dvwa/login.php"
    data = {
        "username": "admin",
        "password": "password",
        "Login": "Login"
    }
    session.post(login_url, data=data)
    return session
