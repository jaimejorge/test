#!/usr/bin/env python

from flask import Flask, request
import json
import sqlite3
import random

app = Flask('bank')

db = sqlite3.connect(':memory:', isolation_level=None)
c = db.cursor()

c.execute('CREATE TABLE accounts (currency text, ammount int)')


@app.route("/Status")
def status():
    return "OK"

@app.route("/healthcheck")
def healthcheck():
    return "OK"

@app.route('/account', methods=['POST'])
def post_account():
    try:
        currency = request.json['currency']
        c.execute('INSERT INTO accounts (currency, ammount) VALUES (?, 0)', (currency,))
        d = {
            'id' : c.lastrowid,
            'currecy' : currency,
            'ammount' : 0
        }
        return json.dumps(d),201 # CREATED
    except:
        return '',417 # EXPECTATION FAILED


@app.route('/account/<int:id>', methods=['GET'])
def get_account_id(id):
    try:
        c.execute('SELECT rowid,* FROM accounts WHERE rowid = ?', (id,))
        row = c.fetchone()
        if row == None:
            return '',416 # REQUEST RANGE NOT SATISFABLE
        d = {
            'id' : row[0],
            'currency' : row[1],
            'ammount' : row[2]
        }
        return json.dumps(d),200
    except:
        return '',417 # EXPECTATION FAILED


@app.route('/account/<int:id>/deposit', methods=['POST'])
def post_account_deposit(id):
    try:
        ammount = int(request.json['ammount'])
        if ammount <= 0:
            return '',401 # UNAUTHORIZED

        c.execute('SELECT rowid,* FROM accounts WHERE rowid = ?', (id,))
        row = c.fetchone()
        if row == None:
            return '',416 # REQUEST RANGE NOT SATISFABLE

        c.execute('UPDATE accounts SET ammount = ? WHERE rowid = ?', (row[2]+ammount, row[0]))
        return '',201 # CREATED
    except:
        return '',417 # EXPECTATION FAILED


@app.route('/account/<int:id>/withdraw', methods=['POST'])
def post_account_withdraw(id):
    try:
        ammount = int(request.json['ammount'])
        if ammount <= 0:
            return '',401 # UNAUTHORIZED

        c.execute('SELECT rowid,* FROM accounts WHERE rowid = ?', (id,))
        row = c.fetchone()
        if row == None:
            return '',416 # REQUEST RANGE NOT SATISFABLE

        if row[2] < ammount:
            return '',401 # UNAUTHORIZED

        c.execute('UPDATE accounts SET ammount = ? WHERE rowid = ?', (row[2]-ammount, row[0]))
        return '',201 # CREATED
    except:
        return '',417 # EXPECTATION FAILED


@app.route('/transfer', methods=['POST'])
def post_transfer():
    try:
        ammount = int(request.json['ammount'])
        if ammount <= 0:
            return '',401 # UNAUTHORIZED

        src = request.json['src']
        dst = request.json['dst']

        c.execute('SELECT rowid,* FROM accounts WHERE rowid = ?', (src,))
        src_row = c.fetchone()
        if src_row == None:
            return '',416 # REQUEST RANGE NOT SATISFABLE

        if src_row[2] < ammount:
            return '',401 # UNAUTHORIZED

        c.execute('SELECT rowid,* FROM accounts WHERE rowid = ?', (dst,))
        dst_row = c.fetchone()
        if dst_row == None:
            return '',416 # REQUEST RANGE NOT SATISFABLE

        if src_row[1] != dst_row[1]:
            return '',401 # UNAUTHORIZED

        c.execute('UPDATE accounts SET ammount = ? WHERE rowid = ?', (src_row[2]-ammount, src_row[0]))
        c.execute('UPDATE accounts SET ammount = ? WHERE rowid = ?', (dst_row[2]+ammount, dst_row[0]))
        return '',201 # CREATED
    except:
        return '',417 # EXPECTATION FAILED


if __name__ == '__main__':
    app.run(host='0.0.0.0')
