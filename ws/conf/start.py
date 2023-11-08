import json
import os
from util import ParseJson, SetupFailed
import beauti
import argparse 


fw = beauti.CostumePrint()

class Setup:
    def __init__(self, filename='db.json'):
        self.filename = filename
        self.default_data = {
            "login_info": {
                "username": "",
                "password": "",
                "success": "False"
            },
            "naloge": [],
            "vaje": []
        }
    
    def create_file(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as file:
                json.dump(self.default_data, file, indent=4)
            fw.info(f"'{self.filename}' created with default structure.", 2)
            return True
        else:
            fw.info(f"'{self.filename}' already exists.", 2)
            return False

    # Example
    # setup = StartSetup()
    # setup.create_file()


class Start_helper:
    def __init__(self) -> None:
        pass
    
    def Chek()->bool:
        """Checks if db.json exists and its data is not DEFAULT

        Returns:
            bool: True if db.json exists and its data is not DEFAULT, False otherwise
        """
        demon = Setup()
        runner = ParseJson('db.json')
        try:
            li = runner.read_login_info()
            return True if li[0] != '' and li[1] != '' else False
        except Exception as e:
            fw.info(e, 2)
            return False
        
    def Reset_login_info(file:object, user:str, password:str):
        """Resets users login info

        Args:
            user (str): username
            pasword (str): password
        """
        file.write_login_info(user, password)
        
    
    def Args():
        """Prompts user for login info if db.json does not exist or its data is DEFAULT.

        Returns:
            None: if login info is already stored in db.json
            username, password: if login info is not stored in db.json 
        """
        
        fw.info("Parsing arguments", 2, "Username and password are stored localy so no need to enter them every time nor worry about them being stolen.")
        parser = argparse.ArgumentParser(description='Start program')
        parser.add_argument('-m', '--manual', action='store_true', help='Setup program manually (needs no other args)')
        parser.add_argument('-s', '--setup', action='store_true', help='Setup program')
        parser.add_argument('-u', '--username', type=str, help='Username for login')
        parser.add_argument('-p', '--password', type=str, help='Password for login')
        
        args = parser.parse_args()
        fw.info("Checking if db.json exists and its data is not DEFAULT", 2, "If it does not exist it will be created with default structure.")
                    
        return args
    # add function to test login with username and password

class start:
    def __init__(self) -> None:
        pass

    def Exe(self):
        """Executes setup of program

        Args:
            args (argparse.Namespace): arguments from Args function
        """
        args = Start_helper.Args()
        
        if args.setup:
            if not args.username or  not args.password:
                fw.info("Username or password not provided", 2)
                fw.info("Program setup aborted", 2, "Error: incorrect arguments")
                exit()
                
        if args.setup:
            fw.info("Setting up program", 2)
            setup = Setup()
            if Start_helper.Chek():
                fw.info("db.json exists/was created and data is not DEFAULT", 2)
                rst = fw.get_info("Would you wish to reset login info? [y/n]")
                if rst == 'y':
                    js = ParseJson('db.json')
                    Start_helper.Reset_login_info(js, args.username, args.password)
                    fw.info("Login info reseted", 2)
                else:
                    fw.info("If you wish to run the script user -m/--manual argument", 2)
                    return None
            else:
                fw.info("db.json does not exist", 2)
                fw.info("Creating db.json", 2)
                setup.create_file()
                try:
                    js = ParseJson('db.json')
                    try:
                        js.write_login_info(args.username, args.password)
                        fw.info("Login info stored", 2)
                    except Exception as e:
                        fw.info(e, 2, "Raising exception")
                        raise SetupFailed("File could not be created")
                except SetupFailed as e:
                    fw.info(e, 2, "Exiting program")
                    exit()
            fw.info("Program setup complete", 2)
        elif args.manual:
            fw.info("Manual setup selected...exiting setup sript", 2, "Test login with username and password") 
        else:
            fw.info("Program setup aborted", 2, "Error: incorrect arguments")
        username, password = ParseJson('db.json').read_login_info()
        fw.info("Attempting to login", 2, f"Using [{username}] as username and [{password}] as password")
        success = self.attempt_login()

        if success:
            fw.info("Login successful", 2)
            fw.info("Proceeding to main script", 2)
            js = ParseJson('db.json')
            js.write_state("True")
            return True
        else:
            fw.info("Login failed", 2)
            exit()

    def attempt_login(self)->None:
        """Attempts to login with username and password

        Returns:
            Modified json file with success status
        """
        import web

        ws = web.Login()
        return ws.login()        
