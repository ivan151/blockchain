from flask import Flask
from flask import render_template, redirect, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
import random
import uuid
import json
import os
import hashlib

blockchain_dir = os.curdir + '/blockchain/'

def get_hash(filename):
    #takes file's name and returns hash,using hashlib library
    file = open(blockchain_dir + filename,'rb').read()
    return hashlib.md5(file).hexdigest()



def int_and_sort(list_of_strings):
    #takes a list of strings, returns a sorted list of integers
    list_of_int = list(map(int,list_of_strings))
    sorted_list_of_int = sorted(list_of_int)
    return sorted_list_of_int

def check_integrity():
    # get hash of the previous block
    # again count its hash
    # compare results
    files = int_and_sort(os.listdir(blockchain_dir))
    results = []
    for filename in files[1:]:
        file_hash = json.load(open(blockchain_dir + str(filename)))['hash']
        prev_file = str(filename - 1)
        actual_hash = get_hash(prev_file)
        if file_hash == actual_hash:
            result = 'ok'
        else:
            result = 'corrupted'
        results.append({'block': prev_file, 'result': result})
    return results

def write_block(name, amount, to_whom, prev_hash=''):
    files = int_and_sort(os.listdir(blockchain_dir)) 
    last_file = files[-1]
    filename = str(last_file + 1)
    prev_hash = get_hash(str(last_file))
    data = {'name': name,
            'amount': amount,
            'to_whom': to_whom,
            'hash': prev_hash}
    with open(blockchain_dir + filename, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

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


def create_key():
    key = str(uuid.uuid4())
    return key


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        new_user = User(name=name, public_key=create_key(),
                        private_key=create_key(), balance=100)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')
    else:
        all_users = User.query.order_by(User.id).all()
        return render_template('index.html', users=all_users)

@app.route('/create/')
def create_user():
    if request.method == 'POST':
        name = request.form['name']
        new_user = User(name=name, public_key=create_key(),
                        private_key=create_key(), balance=100)
        db.session.add(new_user)
        db.session.commit()
        return redirect('create.html')
    else:
        all_users = User.query.order_by(User.id).all()
        return render_template('create.html', users=all_users)

@app.route('/transaction/', methods=['GET', 'POST'])
def transaction():
    if request.method == 'POST':
        session['sender_public_key'] = request.form['from']
        session['receiver_public_key'] = request.form['to']
        session['amount'] = request.form['amount']
        return redirect(url_for('.private'))
    elif request.method == 'GET':
        return render_template('transactions.html')


@app.route('/transaction/private/', methods=['GET', 'POST'])
def private():
    amount = session.get('amount','hren')
    sender_public_key = session.get('sender_public_key','hren')
    receiver_public_key = session.get('receiver_public_key','hren')
    if request.method == 'GET':
        return render_template('private.html', amount = amount, from_whom = sender_public_key, to_whom = receiver_public_key )
    elif request.method == 'POST':
        sender = User.query.filter_by(public_key=sender_public_key).first()
        receiver = User.query.filter_by(public_key=receiver_public_key).first()
        input_private_key=request.form['private']
        if input_private_key == sender.private_key:
            sender.balance=sender.balance - int(amount)
            receiver.balance=receiver.balance + int(amount)
            conf="Transactions added to blockchain!"
            db.session.commit()
            return render_template('private.html', confirmation=conf)
        else:
            wrong='The Private Key is incorrect'
            return render_template('private.html', wrong=wrong)




if __name__ == "__main__":
    app.run(debug=True)
