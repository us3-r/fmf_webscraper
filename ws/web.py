import requests
from bs4 import BeautifulSoup
from util import ParseJson, LoginFailed
from beauti import *
from conf.start import start

js = ParseJson('db.json')
fw = CostumePrint()


class Login:

    global response

    def __init__(self):
        self.session = requests.Session()
        self.username, self.password = js.read_login_info()
        self.login_url = 'https://ucilnica.fmf.uni-lj.si/login/index.php'

    def login(self)->bool:
        """Attempts to log in to the website

        Raises:
            LoginFailed: if login fails

        Returns:
            True if login was successful, False otherwise
        """
        try:
            # Attempt to log in with only username and password
            fw.info("Trying to log in with only username and password", 0)
            response = self.session.post(self.login_url, data={'username': self.username, 'password': self.password})
            fw.info(fw.explain_status_code(response.status_code), 1)
            if response.url == self.login_url:
                fw.info("Login failed", 2)
                fw.info("Proceeding to login with tokens",0)
                raise LoginFailed

        except LoginFailed:
            # If previous login attempt failed, try again with tokens
            # Get the login page to retrieve any necessary tokens if needed
            fw.info("Trying to log in with tokens", 0)
            response = self.session.get(self.login_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the hidden fields in the form and include them in your login payload
            hidden_inputs = soup.find_all("input", type="hidden")
            login_payload = {input.get("name"): input.get("value") for input in hidden_inputs}
            login_payload['username'] = self.username
            login_payload['password'] = self.password

            # Attempt to log in
            response = self.session.post(self.login_url, data=login_payload)
            fw.info(fw.explain_status_code(response.status_code),1)
        finally:
            if response.url != self.login_url:
                self.get_class_ids()
            else:
                return False


    def get_class_ids(self) -> list:
        """Gets all the class ids from the website

        Returns:
            list: list of class ids
        """
        fw.info("Getting class ids", 0)
        response = self.session.get('https://ucilnica.fmf.uni-lj.si/')

        # checks if get request was successful and returns list of class ids
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            course_elements = soup.find_all('a', class_='aalink')
            class_ids = [element['href'].split('=')[1] for element in course_elements if 'course' in element['href']]
            self.verify_id(class_ids)
            return class_ids
        else:
            fw.error(f"Failed to retrieve content, status code: {response.status_code}")
            return []

    def verify_id(self, id:list)->bool:
        """Checks if id is valid

        Args:
            id (list): list of class ids

        Returns:
            bool: True if id is valid, False otherwise
        """
        fw.info("Verifying class urls", 0)
        js = ParseJson('db.json')
        for i in id:
            url = f'https://ucilnica.fmf.uni-lj.si/course/view.php?id={i}'
            response = self.session.get(url)
            if response.status_code == 200:
                fw.info(f"{i} is valid", 1)
                name = BeautifulSoup(response.text, 'html.parser').find('h1').text.strip()
                js.write_url(name, {'valid_url': url})
            else:
                fw.error(f"{i} is invalid", 1)
                return False