from flask import Flask
from flask import render_template, redirect, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from functions import node_dirs, write_block, write_block_to_nodes, change_block, get_hash, int_and_sort, check_integrity
from functions import blockchain_dir, nodes_route, restore_integrity, create_private_key, create_public_key
import random
import uuid
import json
import os
import hashlib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SECRET_KEY'] = '3d6f45a5fc12445dbac2f59c3b6c7cb1'
db = SQLAlchemy(app)

SQLALCHEMY_TRACK_MODIFICATIONS = False


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    public_key = db.Column(db.String(100), nullable=False)
    private_key = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Integer)

    def __repr__(self):
        return 'User' + str(self.id)


@app.route('/', methods=['GET'])
def index():
        return render_template('index.html')


@app.route('/create/')
def create_user():
    if request.method == 'POST':
        name = request.form['name']
        new_user = User(name=name, public_key=create_public_key,
                        private_key=create_private_key, balance=100)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/create/')
    else:
        all_users = User.query.order_by(User.id).all()
        return render_template('create.html', users=all_users)


@app.route('/transaction/', methods=['GET', 'POST'])
def transaction():
    users = User.query.all()
    if request.method == 'POST':
        session['sender_public_key'] = request.form['from']
        session['receiver_public_key'] = request.form['to']
        session['amount'] = request.form['amount']
        return redirect(url_for('.private'))
    elif request.method == 'GET':
        return render_template('transactions.html', users = users)


@app.route('/transaction/private/', methods=['GET', 'POST'])
def private():
    amount = session.get('amount')
    sender_public_key = session.get('sender_public_key')
    receiver_public_key = session.get('receiver_public_key')
    sender = User.query.filter_by(public_key=sender_public_key).first()
    #receiver = User.query.filter_by(public_key=receiver_public_key).first()
    if request.method == 'GET':
        return render_template('private.html', amount=amount, 
        from_whom=sender_public_key, to_whom=receiver_public_key, 
        sender_private_key=sender.private_key)
    elif request.method == 'POST':
        input_private_key = request.form['private']
        nodes_numbers = []
        for i in range(1, 7):
            nodes_numbers.append(request.form.get(f'node{i}'))
        if input_private_key == sender.private_key:
            if nodes_numbers.count(None) < 3:
                block_data = write_block(from_who=sender_public_key,
                            to_whom=receiver_public_key, amount=amount)
                write_block_to_nodes(from_who=sender_public_key,
                            to_whom=receiver_public_key, amount=amount)
                return render_template('private.html', block = block_data, confirmation='Transaction added to the blockchain!')
            else:
                return render_template('private.html', deny = "Not enough nodes to change the blockchain!")
        else:
            wrong = 'The Private Key is incorrect'
            return render_template('private.html', wrong=wrong)


@app.route('/blockchain/', methods=['GET'])
def blockchain():
    blocks_dict = {}
    files = int_and_sort(os.listdir(blockchain_dir))
    for filename in reversed(files[1:]):
        block = json.load(open(blockchain_dir + str(filename), 'rb'))
        blocks_dict[filename] = block
    return render_template('blockchain.html', blocks=blocks_dict)


@app.route('/integrity/', methods=['GET'])
def integrity():
    results = check_integrity()
    return render_template('integrity.html', results=results)


@app.route('/blockchain/edit/<int:num>', methods=['GET', 'POST'])
def edit(num):
    block_number = num
    files = int_and_sort(os.listdir(blockchain_dir))
    last_file = files[-1]
    blockchain_filename = blockchain_dir + str(num)
    block = json.load(open( blockchain_filename, 'rb'))
    if request.method == 'GET':
        return render_template('edit.html', block=block, number=num, last_file=last_file)
    else:
        if block_number == last_file:

            nodes_numbers = []
            for i in range(1, 7):
                nodes_numbers.append(request.form.get(f'node{i}'))
            if nodes_numbers.count(None) < 3:
                from_who = request.form['from']
                to_whom = request.form['to']
                amount = request.form['amount']
                new_hash = request.form['hash']
                change_block(block_number, from_who,  to_whom, amount, new_hash)
                return render_template('edit.html', edited='BLOCK IS CHANGED!', number=num, block=block,last_file = last_file)
            else:
                return render_template('edit.html', deny='YOU CANT CHANGE THIS BLOG WITHOUT ACCESS TO ENOUGH NUMBER OF NODES!', number=num, block=block,last_file = last_file)
        else:
            from_who = request.form['from']
            to_whom = request.form['to']
            amount = request.form['amount']
            new_hash = request.form['hash']
            change_block(block_number, from_who,  to_whom, amount, new_hash)
            return render_template('edit.html', edited='You have changed the block!', number=num, block=block)


@app.route('/nodes/<int:i>/')
def node(i):
    n = i
    if n in range(1, len(node_dirs())+1):
        node = nodes_route + str(n) + '/'
        files = int_and_sort(os.listdir(node))
        blocks_dict = {}
        for filename in reversed(files[1:]):
            block = json.load(open(node + str(filename), 'rb'))
            blocks_dict[filename] = block
        return render_template('node.html', blocks=blocks_dict, number=n)

@app.route('/restore', methods=['GET'])
def restore():
    restore_integrity()
    return redirect('/integrity/')
   
   
if __name__ == "__main__":
    app.run(debug=True)
