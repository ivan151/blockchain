import json

from functions import change_block

filename = 'jopa.txt'
from_who = 'ivan'                                                                        
to_whom = 'petr'                                                                         
new_hash = 'cnancabjcbasbcajsbchjabc'                                                    
amount = 500        

change_block(filename, from_who,  to_whom, amount, new_hash)