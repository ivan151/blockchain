import random
import uuid
import json
import os
import hashlib


blockchain_dir = os.curdir + '/blockchain/'
nodes_route = os.curdir + '/nodes/'

def get_hash(filename):
    #takes file's name and returns hash,using hashlib library
    file = open(blockchain_dir + filename,'rb').read()
    return hashlib.md5(file).hexdigest()

def create_key():
    key = uuid.uuid1().hex 
    return key

def int_and_sort(list_of_strings):
    #takes a list of strings, returns a sorted list of integers
    list_of_int = list(map(int,list_of_strings))
    sorted_list_of_int = sorted(list_of_int)
    return sorted_list_of_int

files = int_and_sort(os.listdir(blockchain_dir))

def node_dirs():
    node_dirs_list = []
    for name in sorted(os.listdir(nodes_route)):
        node_dirs_list.append(nodes_route + name + '/')
    return node_dirs_list
    
def write_block(from_who,  to_whom, amount, prev_hash=''):
    last_file = files[-1]
    filename = str(last_file + 1)
    prev_hash = get_hash(str(last_file))
    data = {'from': from_who,
            'to': to_whom,
            'amount': amount,
            'hash': prev_hash}
    with open(blockchain_dir + filename, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def write_block_to_nodes(from_who,  to_whom, amount, prev_hash=''):
    for i in node_dirs:
        node = nodes_route + str(i) + '/'
        files = int_and_sort(os.listdir(node))
        last_file = files[-1]
        filename = str(last_file + 1)
        prev_hash = get_hash(str(last_file))    
        data = {'from': from_who,
            'to': to_whom,
            'amount': amount,
            'hash': prev_hash}
        with open(node + '/' + filename, 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

def genesis():
    #return the blockchain and nodes to their original state
    for file in files[1:]:
        os.remove(blockchain_dir+str(file))
    for i in node_dirs:
        node = nodes_route + str(i) + '/'
        node_files = sorted((os.listdir(node)))
        for file in node_files
    
    return(os.listdir(blockchain_dir))