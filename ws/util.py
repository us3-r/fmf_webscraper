import json
import os

class ParseJson:
    def __init__(self, filename):
        self.filename = filename
    
    def write_login_info(self, username, password):
        data = self._load_data()
        data['login_info']['username'] = username
        data['login_info']['password'] = password
        self._write_data(data)

    def write_state(self, state):
        data = self._load_data()
        data['login_info']['success'] = state
        self._write_data(data)
    
    def write_url(self, name,url):
        data = self._load_data()
        if not any(name in entry for entry in data['urls']):
            data['urls'].append({name: url})
            self._write_data(data)
        else:
            pass

    def write_json(self, cont_name:str, id:int, name:str, description:str):
        data = self._load_data()
        
        try:    
            data.setdefault(cont_name, []).append({
                'id': id,
                'name': name,
                'description': description
            })
            if not isinstance(cont_name, str):
                raise TypeError("cont_name must be a string but is {}".format(type(cont_name)))
        
        except TypeError as e:
            print(e)
            exit()

        self._write_data(data)

    def read_login_info(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            login_info = json.load(file)['login_info']
            username = login_info['username']
            password = login_info['password']
        return username, password

    def read_state(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            login_info = json.load(file)['login_info']
            state = login_info['success']
        return state

    # def write_json_vaje(self, id, name, description):
    #     data = self._load_data()
    #     data.setdefault('vaje', []).append({
    #         'id': id,
    #         'name': name,
    #         'description': description
    #     })
    #     self._write_data(data)

    def _load_data(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            return json.load(file)

    def _write_data(self, data):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    # Examples
    # parser = ParseJson('db.json')
    # username, password = parser.read_login_info()
    # parser.write_json_naloga(1, 'Naloga 1', 'Opis naloge 1')
    # parser.write_json_vaje(1, 'Vaja 1', 'Opis vaje 1')

class LoginFailed(Exception):
    # Class used for raising an exception when login fails
    pass

class SetupFailed(Exception):
    # Class used for raising an exception when setup fails
    pass