import random
import uuid
import json
import os
import hashlib

blockchain_dir = os.curdir + '/blockchain/'
nodes_route = os.curdir + '/nodes/'
reserved_dir = blockchain_dir + '/reserved/'

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



def node_dirs():
    node_dirs_list = []
    for name in sorted(os.listdir(nodes_route)):
        node_dirs_list.append(nodes_route + name + '/')
    return node_dirs_list
    
def write_block(from_who,  to_whom, amount, prev_hash=''):
    files = int_and_sort(os.listdir(blockchain_dir))
    last_file = files[-1]
    filename = str(last_file + 1)
    prev_hash = get_hash(str(last_file))
    data = {'from': from_who,
            'to': to_whom,
            'amount': amount,
            'hash': prev_hash}
    with open(blockchain_dir + filename, 'w+') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    return data

def reserve(num):
    blockchain_filename = blockchain_dir + str(num)
    reserved_data = json.load(open( blockchain_filename, 'rb'))
    reserve_block_dir = reserved_dir + str(num) + '/'
    files = int_and_sort(os.listdir(reserve_block_dir))
    last_file = files[-1]
    filename = str(last_file + 1)
    with open(filename, 'w+') as file:
        json.dump(reserved_data, file, indent=4, ensure_ascii=False)

def change_block(num, from_who,  to_whom, amount, new_hash):
    data = {'from': from_who,
            'to': to_whom,
            'amount': amount,
            'hash': new_hash }
    blockchain_filename = blockchain_dir + str(num)
    reserve(num)
    with open(blockchain_filename, 'w+') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    for node in node_dirs():
        nodes_filename = node + '/' + str(num)
        with open(nodes_filename, 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

def write_block_to_nodes(from_who,  to_whom, amount, prev_hash=''):
    for node in node_dirs():
        node_files = sorted((os.listdir(node)))
        last_file = node_files[-1]
        filename = str(int(last_file) + 1)
        prev_hash = get_hash(last_file)    
        data = {'from': from_who,
            'to': to_whom,
            'amount': amount,
            'hash': prev_hash}
        with open(node + '/' + filename, 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

def genesis():
    #return the blockchain and nodes to their original state
    files = int_and_sort(os.listdir(blockchain_dir))
    for filename in files[1:]:
        os.remove(blockchain_dir+str(filename))
    for node in node_dirs():
        node_files = sorted((os.listdir(node)))
        for filename in node_files[1:]:
            os.remove(node+filename)
    
    return(os.listdir(blockchain_dir))