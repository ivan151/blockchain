from functions import genesis
from functions import write_block

from_who = 'ivan'
to_whom = 'petr'
amount = 1002

def create_dir(num):
    if not os.path.exists('{}'.format(num)):
        os.makedirs('{}'.format(num))
    return 'Done!')

#write_block(from_who,to_whom,amount)
genesis()
create()