from conf.start import start
from util import ParseJson

success = start().Exe()

if success:
    # execute program
    pass
else:
    js = ParseJson('db.json')
    if js.read_state() == "True":
        # execute program
        pass
    else:
        # exit program
        pass
    