#!/bin/python

import os  # Will I need it??
import re  # And this??
import sqlite3
from datetime import date

database = 'ketocalc.db'


def products():
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('SELECT * FROM products')
    print('Values per 100g')
    while True:
        result = c.fetchone()
        if result is None:
            break
        print(result)
    c.close()
    main()


def one_product():
    conn = sqlite3.connect(database)
    c = conn.cursor()  # Cursor for if cond to check whenever product is in database
    cc = conn.cursor()  # Second cursor to fetchall results is it necessarry? Name is primary key anyway, so there can not be 2 products with the same name - since search implementation 2 cursors necessary ARE THEY - ? - looks like yes, since program does not fetch all but one by one
    print('Enter product name (also searches for products containg string)')
    product = input().lower().capitalize()
    c.execute('SELECT * FROM products WHERE name LIKE \'%' + product + '%\'')
    result = c.fetchone()
    if result is None:
        print('Product not in database')
    else:
        cc.execute('SELECT * FROM products WHERE name LIKE \'%' + product + '%\'')
        while True:
            # Fetch one by one to avoid using pretty printing - keeps list alike look
            results = cc.fetchone()
            if results is None:
                break
            # Needs to be change to pretty print for indents and shit
            # from pprint import pprint
            # Future development
            print(results)
    c.close()
    cc.close()
    main()


def add_product():
    conn = sqlite3.connect(database)
    print('Enter product name:')
    name = input().lower()
    name = name.capitalize()
    print('Enter calories value (per 100g):')
    kcal = input()
    print('Enter protein value (per 100g):')
    protein = input()
    print('Enter fat value (per 100g):')
    fat = input()
    print('Enter fibre value (per 100g):')
    fibre = input()
    print('Enter carbs value (per 100g):')
    carbs = input()
    print('Enter grams per pack:')
    GPP = input()
    print('Enter price per pack (in local currency):')
    PPP = input()

    c = conn.cursor()
    params = {'name': name, 'kcal': kcal, 'protein': protein, 'fat': fat, 'fibre': fibre, 'carbs': carbs, 'price': PPP, 'grams': GPP}
    c.execute('INSERT OR IGNORE INTO products VALUES (:name, :kcal, :protein, :fat, :fibre, :carbs, :grams, :price)', params)
    conn.commit()
    c.close()
    main()


def today_table():
    conn = sqlite3.connect(database)
    c = conn.cursor()
    print('Which day would you like to check? YYYY-MM-DD')
    date = input()
    try:
        c.execute('SELECT * FROM \'' + date + '\'')
    except sqlite3.OperationalError:
        print('There is no table for %s' % date)
        main()
    print(c.fetchall())


def today_eaten():
    today = str(date.today())
    daily_intake()
    conn = sqlite3.connect(database)
    c = conn.cursor()
    print('Which product have you eaten?')
    product = input().lower().capitalize()
    p_query = 'SELECT * FROM products WHERE name=\'' + product + '\''
    c.execute(p_query)
    p_tuple = c.fetchone()
    if p_tuple is None:
        print('Product is not in product list')
        main()
    # Take tuple apart
    name = p_tuple[0]
    calories = p_tuple[1] / 100
    protein = p_tuple[2] / 100
    fat = p_tuple[3] / 100
    fibre = p_tuple[4] / 100
    carbs = p_tuple[5] / 100
    grams = p_tuple[6]
    price = p_tuple[7]
    if grams is not None or grams is not '0':
        gram_price = price / grams
    print('How many grams have you used or what amount have you used?')
    used_amount = int(input())
    calories = calories * used_amount
    protein = protein * used_amount
    fat = fat * used_amount
    fibre = fibre * used_amount
    carbs = carbs * used_amount
    used_cost = gram_price * used_amount
    used_cost = round(used_cost, 2)
    params = {'name': name, 'calories': calories, 'protein': protein, 'fat': fat, 'fibre': fibre, 'carbs': carbs, 'cost': used_cost, 'grams': used_amount}
    add_q = 'INSERT INTO \'' + today + '\' VALUES (:name, :calories, :protein, :fat, :fibre, :carbs, :grams, :cost)'
    c.execute(add_q, params)
    conn.commit()
    c.close()
    main()

def daily_intake():
    today = str(date.today())
    conn = sqlite3.connect(database)
    c = conn.cursor()
    new = 'CREATE TABLE IF NOT EXISTS \'' + today + '\' (name text, kcal real, protein real, fat real, fibre real, carbs real, grams real, cost real)'
    c.execute(new)
    conn.commit()
    c.close()


def main():
    print('What would you like to do? \n 1 - List products \n 2 - List specific product \n 3 - Add products \n 4 - Check intake from specific date \n 5 - Add product to todays\' table \n 9 - Exit')
    action = input()
    if action == '3':
        add_product()
    elif action == '1':
        products()
    elif action == '4':
        today_table()
    elif action == '2':
        one_product()
    elif action is '5':
        today_eaten()
    elif action == '9':
        exit()


main()
