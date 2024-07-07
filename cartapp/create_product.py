import pandas as pd
import sys
import os
import sqlite3


# connect database
con = sqlite3.connect('D:/django_cart/db.sqlite3')
cursorObj = con.cursor()

# read dataset
df = pd.read_csv('D:/django_cart/data.csv')

for link,name,price,image,description in zip(df['link'],df['name'],df['price'],df['image'],df['seller_board']):
    if '~' in price:
        price = price[0].replace(',','')
    else:
        price = price.replace(',','')
    image_name = image.split('/')[-1]
    query = "INSERT INTO Product (prod_description, prod_img, prod_link, prod_name, prod_price) VALUES (?, ?, ?, ?, ?)"
    cursorObj.execute(query, (description, image_name, link, name, price))
    con.commit()
# create products