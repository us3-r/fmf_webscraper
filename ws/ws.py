import requests
from bs4 import BeautifulSoup
from classes import ParseJson, LoginFailed
from beauti import CostumePrint

js = ParseJson('db.json')
fw = CostumePrint()

# Start a session
session = requests.Session()
u,p = js.read_login_info()
# This URL will be the login page's URL
login_url = 'https://ucilnica.fmf.uni-lj.si/login/index.php'

try:
    # Attempt to log in with only username and password
    fw.print_info("Trying to log in with only username and password", False)
    response = session.post(login_url, data={'username': u, 'password': p})
    fw.print_info(response.url, True, response.status_code)
    if response.url == login_url:
        fw.print_info("Login failed", False, "Proceeding to login with tokens")
        raise LoginFailed

except LoginFailed:
    # If previous login attempt failed, try again with tokens
    # Get the login page to retrieve any necessary tokens if needed
    fw.print_info("Trying to log in with tokens", False)
    response = session.get(login_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the hidden fields in the form and include them in your login payload
    hidden_inputs = soup.find_all("input", type="hidden")
    login_payload = {input.get("name"): input.get("value") for input in hidden_inputs}
    login_payload['username'] = u
    login_payload['password'] = p

    # Attempt to log in
    response = session.post(login_url, data=login_payload)
    fw.print_info(response.url, True, response.status_code)
finally:
    if response.url != login_url:
        fw.print_info("Login successful", False)
    else:
        fw.print_info("Login failed", False, "Exiting program")
        exit()
