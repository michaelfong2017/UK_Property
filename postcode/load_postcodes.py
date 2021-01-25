#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: michael
"""

import MySQLdb
import MySQLdb.cursors
conn = MySQLdb.connect(host='localhost', db='uk_property', 
                       user='root', passwd='P@ssw0rd',
                       cursorclass=MySQLdb.cursors.DictCursor)

postcode_dict = dict()
try:
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM postcode")
        db_nodes = cursor.fetchall()
 
        for node in db_nodes:
            postcode_dict[node['postcode']] = node['postcodeEncoded']
            
finally:
    conn.close()
  
print()
print(len(postcode_dict))

import pickle
a_file = open("postcodes.pkl", "wb")
pickle.dump(postcode_dict, a_file)
a_file.close()