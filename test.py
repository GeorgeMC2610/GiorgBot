from datetime import datetime
from dateutil import parser
import re

perif = "ΧΩΡΑ 22/02/2022"
reg = re.search(r"(ΟΛΟ)|(ΟΛΟΙ)|(ΟΛΑ)|(ΣΥΝΟΛΟ)|(ΣΥΝΟΛΙΚΑ)|(ΕΛΛΑΔΑ)|(ΧΩΡΑ)|(ΠΑΝΤΕΣ)", perif)

print( len(perif[ reg.end() + 1 : ]) ) 