from functions import genesis
from functions import write_block

from_who = 'ivan'
to_whom = 'petr'
amount = 1002

write_block(from_who,to_whom,amount)
write_block_to_node(node, from_who,  to_whom, amount)
#genesis()