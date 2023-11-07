import requests
from bs4 import BeautifulSoup
from classes import ParseJson, LoginFailed

js = ParseJson('db.json')


# Start a session
session = requests.Session()
u,p = js.read_login_info()
# This URL will be the login page's URL
login_url = 'https://ucilnica.fmf.uni-lj.si/login/index.php'

try:
    # Attempt to log in with only username and password
    print("Trying to log in without tokens")
    response = session.post(login_url, data={'username': u, 'password': p})
    print(response.status_code)
    print(response.url)
    if response.url == login_url:
        raise LoginFailed

except LoginFailed:
    # If previous login attempt failed, try again with tokens
    # Get the login page to retrieve any necessary tokens if needed
    print("Trying to log in with tokens")
    response = session.get(login_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the hidden fields in the form and include them in your login payload
    hidden_inputs = soup.find_all("input", type="hidden")
    login_payload = {input.get("name"): input.get("value") for input in hidden_inputs}
    login_payload['username'] = u
    login_payload['password'] = p

    # Attempt to log in
    response = session.post(login_url, data=login_payload)
    print(response.status_code)
    print(response.url)
finally:
    if response.url != login_url:
        print("Login successful")
    else:
        print("Login failed")


# trgt_url = 'https://ucilnica.fmf.uni-lj.si/course/view.php?id=119'

# response = session.get(trgt_url)
# print(response.status_code)
# print(response.url)
# res_text = response.text
# soup = BeautifulSoup(res_text, 'html.parser')

# search_elem = soup.find_all('span', class_='instancename')
# print(len(search_elem))
# for elem in search_elem:
#     if 'NALOGA' in elem.text:
#         print(elem.text)
