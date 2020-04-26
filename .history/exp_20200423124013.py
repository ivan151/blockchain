import json

def change_block(filename, from_who,  to_whom, amount, new_hash):
    data = {'from': from_who,
    'to': to_whom,
    'amount': amount,
    'hash': new_hash }
    with open(filename, 'w+') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

filename = 'jopa.txt'
from_who = 'ivan'                                                                        
to_whom = 'petr'                                                                         
new_hash = 'cnancabjcbasbcajsbchjabc'                                                    
amount = 500        

change_block(filename, from_who,  to_whom, amount, new_hash)