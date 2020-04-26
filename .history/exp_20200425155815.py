from functions import genesis
from functions import write_block, change_block, repair_integrity
import os

from_who = 'ivan'
to_whom = 'petr'
amount = 1002

def create_dir(num):
    if not os.path.exists('{}'.format(num)):
        os.makedirs('{}'.format(num))
    return ('Done!')

#write_block(from_who,to_whom,amount)
genesis()
#create_dir(2)

#repair_integrity()