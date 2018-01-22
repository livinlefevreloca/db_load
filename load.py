#!Python3
#load.py - module for loading data into db in different configuartions  

import psycopg2 as pg
from psycopg2 import sql
from datetime import datetime
import os, re

def db_connect():
    #connect to DB and return connection instance
    conn = pg.connect(database=os.environ['DB'], user=os.environ['USER'], password=os.environ['PW'], host=os.environ['ENDPNT'] ) 
    return conn
def db_end_session(connection, cursor):
    #commit changes to DB and end session gracefully. TO BE USED AT THE END OF EVERY SESSION
    connection.commit()
    cursor.close()
    connection.close()
    
    
def check_for_existing(building_name, equipment_name):
    #check if the piece of equipment being loaded exists already and if the building it belongs to exisits
    b_exists = True
    e_exists = True
    conn_inst = db_connect()
    cur = conn_inst.cursor()
    cur.execute("SELECT * FROM buildings WHERE address =(%s);", (building_name,))
    if(cur.fetchone() == None):
        b_exists = False
        e_exists = False
        db_end_session(conn_inst, cur)
        return [b_exists, e_exists]
    cur.execute("SELECT * FROM equipment WHERE equipment_id = (%s) AND building_address=(%s);", (equipment_name, building_name))
    if(cur.fetchone() == None):
        e_exists = False
    db_end_session(conn_inst, cur)
    return [b_exists, e_exists]
    
def load_building(building_name, engineer_name):
    #Add new building to buildings DB
    conn_inst = db_connect()
    cur = conn_inst.cursor()
    cur.execute("INSERT INTO buildings (address, engineer) VALUES (%s, %s);",(building_name, engineer_name))
    db_end_session(conn_inst, cur)
    return(True)

def read_in_file(filepath):
    #read data in from csv file (used for creating new equipment tables) so data can be cleaned and re-typed
    with open(filepath, 'r') as equip_file:
        headers = equip_file.readline().split(',')
        data = []
        for line in equip_file:
            row = line.split(',')
            data.append(row)
    return (data, headers)


def clean_inputs(data, headers):
    # remove extraneous charcters and replace '.' with '-' for JSON notation on web app side
    for row in data:
        for j, val in enumerate(row):
            row[j] = val.rstrip()
    for i, head in enumerate(headers):
        headers[i] = head.rstrip().replace('.', '-')
    return (data, headers)   
        
def load_equip(equip_name, table_data, headers):
    #loads extracted file_data into an existing equipment table using the equip_name
    conn_inst = db_connect()
    cur = conn_inst.cursor()
    headers =  ', '.join(headers)
    query = "INSERT INTO " + equip_name + " {} VALUES {};"
    for data in table_data:
        data = ', '.join(data)
        cur.execute(query.format(headers, data))
    db_end_session(conn_inst, cur)       


def create_equip_table(equip_name, headers, data):
    conn_inst = db_connect()
    cur = conn_inst.cursor()
    cur.execute(sql.SQL("CREATE TABLE {} (id serial);").format(sql.Identifier(equip_name)))
    for col in headers:
        cur.execute(sql.SQL("ALTER TABLE {} ADD COLUMN {} text").format(sql.Identifier(equip_name), sql.Identifier(col)))
    db_end_session(conn_inst, cur)
    
def main():
    data, headers = read_in_file(os.path.join(os.getcwd(), 'data/AHU1/AHU1.csv'))
    data, headers = clean_inputs(data, headers)
    create_equip_table("AHU1", headers, data)
    load_equip("AHU1", data, headers)
    
    

    
    



