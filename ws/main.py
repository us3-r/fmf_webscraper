from conf.start import start
from util import ParseJson
from web import Login

success = start().Exe()

if success:
    # execute program
    demon = Login()
    demon.verify_id()
else:
    js = ParseJson('db.json')
    if js.read_state() == "True":
        # execute program
        pass
    else:
        # exit program
        pass
    