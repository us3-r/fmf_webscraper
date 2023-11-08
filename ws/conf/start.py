# write a functionm that cheks for existantc of db.json file and if it does not exist creat it
import json
import os
from classes import ParseJson, SetupFailed
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
                "success": False
            },
            "naloge": [],
            "vaje": []
        }
    
    def create_file(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as file:
                json.dump(self.default_data, file, indent=4)
            fw.print_info(f"'{self.filename}' created with default structure.", 2)
            return True
        else:
            fw.print_info(f"'{self.filename}' already exists.", 2)
            return False

    # Example
    # setup = StartSetup()
    # setup.create_file()


class Start:
    def __init__(self) -> None:
        pass
    
    def Chek(self)->bool:
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
            fw.print_info(e, 2)
            return False
             
        
    def Reset_login_info(self,file:object, user:str, pasword:str):
        """Resets users login info

        Args:
            user (str): username
            pasword (str): password
        """
        file.write_login_info(user, pasword)
        
    
    def Args(self):
        """Prompts user for login info if db.json does not exist or its data is DEFAULT.

        Returns:
            None: if login info is already stored in db.json
            username, password: if login info is not stored in db.json 
        """
        
        fw.print_info("Parsing arguments", 2, "Username and password are stored localy so no need to enter them every time nor worry about them being stolen.")
        parser = argparse.ArgumentParser(description='Start program')
        parser.add_argument('-m', '--manual', action='store_true', help='Setup program manually (needs no other args)')
        parser.add_argument('-s', '--setup', action='store_true', help='Setup program')
        parser.add_argument('-u', '--username', type=str, help='Username for login')
        parser.add_argument('-p', '--password', type=str, help='Password for login')
        args = parser.parse_args()
        fw.print_info("Checking if db.json exists and its data is not DEFAULT", 2, "If it does not exist it will be created with default structure.")
                    
        return args
    
    def Exe(self):
        """Executes setup of program

        Args:
            args (argparse.Namespace): arguments from Args function
        """
        args = self.Args()
        
        if args.setup:
            if not args.username or  not args.password:
                fw.print_info("Username or password not provided", 2)
                fw.print_info("Program setup aborted", 2, "Error: incorrect arguments")
                exit()
                
        if args.setup:
            fw.print_info("Setting up program", 2)
            setup = Setup()
            if self.Chek():
                fw.print_info("db.json exists/was created and data is not DEFAULT", 2)
                rst = fw.get_info("Would you wish to reset login info? [y/n]")
                if rst == 'y':
                    js = ParseJson('db.json')
                    self.Reset_login_info(js, args.username, args.password)
                    fw.print_info("Login info reseted", 2)
                else:
                    return None
            else:
                fw.print_info("db.json does not exist", 2)
                fw.print_info("Creating db.json", 2)
                setup.create_file()
                try:
                    js = ParseJson('db.json')
                    js.write_login_info(args.username, args.password)
                    fw.print_info("Login info stored", 2)
                    raise SetupFailed("File could not be created")
                except SetupFailed as e:
                    fw.print_info(e, 2, "Exiting program")
                    exit()
            fw.print_info("Program setup complete", 2)
        elif args.manual:
            fw.print_info("Manual setup selected...exiting setup sript", 2)
            return 
        else:
            fw.print_info("Program setup aborted", 2, "Error: incorrect arguments")