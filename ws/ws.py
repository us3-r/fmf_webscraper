import requests
from bs4 import BeautifulSoup
from classes import ParseJson, LoginFailed
from beauti import *

js = ParseJson('db.json')
fw = CostumePrint()

# Start a session
session = requests.Session()
u,p = js.read_login_info()
# This URL will be the login page's URL
login_url = 'https://ucilnica.fmf.uni-lj.si/login/index.php'

try:
    # Attempt to log in with only username and password
    fw.info("Trying to log in with only username and password", 0)
    response = session.post(login_url, data={'username': u, 'password': p})
    fw.info(fw.explain_status_code(response.status_code), 1)
    if response.url == login_url:
        fw.info("Login failed", 2)
        fw.info("Proceeding to login with tokens",0)
        raise LoginFailed

except LoginFailed:
    # If previous login attempt failed, try again with tokens
    # Get the login page to retrieve any necessary tokens if needed
    fw.info("Trying to log in with tokens", 0)
    response = session.get(login_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the hidden fields in the form and include them in your login payload
    hidden_inputs = soup.find_all("input", type="hidden")
    login_payload = {input.get("name"): input.get("value") for input in hidden_inputs}
    login_payload['username'] = u
    login_payload['password'] = p

    # Attempt to log in
    response = session.post(login_url, data=login_payload)
    fw.info(fw.explain_status_code(response.status_code),1)
finally:
    if response.url != login_url:
        fw.info("Login successful", 2)
    else:
        fw.info("Login failed", 2, "Exiting program")
        exit()
