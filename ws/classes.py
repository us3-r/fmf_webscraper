import json
import os

class ParseJson:
    def __init__(self, filename):
        self.filename = filename
    
    def read_login_info(self):
        with open(self.filename, 'r') as file:
            login_info = json.load(file)['login_info']
            username = login_info['username']
            password = login_info['password']
        return username, password

    def write_json_naloga(self, id, name, description):
        data = self._load_data()
        data.setdefault('naloge', []).append({
            'id': id,
            'name': name,
            'description': description
        })
        self._write_data(data)

    def write_json_vaje(self, id, name, description):
        data = self._load_data()
        data.setdefault('vaje', []).append({
            'id': id,
            'name': name,
            'description': description
        })
        self._write_data(data)

    def _load_data(self):
        with open(self.filename, 'r') as file:
            return json.load(file)

    def _write_data(self, data):
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)

    # Examples
    # parser = ParseJson('db.json')
    # username, password = parser.read_login_info()
    # parser.write_json_naloga(1, 'Naloga 1', 'Opis naloge 1')
    # parser.write_json_vaje(1, 'Vaja 1', 'Opis vaje 1')

class LoginFailed(Exception):
    # Class used for raising an exception when login fails
    pass


class StartSetup:
    def __init__(self, filename='db.json'):
        self.filename = filename
        self.default_data = {
            "login_info": {
                "username": "",
                "password": ""
            },
            "naloge": [],
            "vaje": []
        }
    
    def create_file(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as file:
                json.dump(self.default_data, file, indent=4)
            print(f"'{self.filename}' created with default structure.")
        else:
            print(f"'{self.filename}' already exists.")

    # Example
    # setup = StartSetup()
    # setup.create_file()