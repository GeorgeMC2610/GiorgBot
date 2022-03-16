from datetime import datetime
from dateutil import parser
import re

rgx = "falkland islands (malvinas)"
ipt = "falkland islands (malvinas)"

if rgx not in ipt:
    print("no")

elif not ipt.startswith(rgx):
    print("no")