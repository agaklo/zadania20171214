from sqlalchemy import *
import random
import json
from pprint import pprint
import argparse

#SQL_CONNECTION="mysql://root:12345678@localhost/test"
SQL_CONNECTION="postgres://cucbxfcf:dfZj-zciA887DdpvM60YMc8nM6rGf5Vz@horton.elephantsql.com:5432/cucbxfcf"
TABLE_NAME='gisstab17'
DEFAULT_RESULT_FILE="result.json"

#mysql create table gisstab17 (id int, val int);

'''
CREATE TABLE gisstab17
( id integer,
  val integer NOT NULL, 
  PRIMARY KEY(id)
);
'''

def insert_data(connection):
    statement = "insert into "+TABLE_NAME+"(id,val) values "
    for i in range(500):
        value = random.randint(0,19);        
        if i != 0:
            statement += ',';
        statement += " (%d, %d)" % (i, value)               
    connection.execute(statement)

def select_data(connection):
    result_set = connection.execute(
        "SELECT val as v, count(*) as c FROM "+TABLE_NAME+" group by val");
    result = {}
    for row in result_set:
        result[ row.v ] = row.c
    return result
        
def write_output(file_name, data):
    with open(file_name, 'w') as f:
        f.write(json.dumps(data))


if __name__== '__main__':
    parser = argparse.ArgumentParser("test")
    parser.add_argument("command", 
	help="Issue command to insert data to database or select statistics", 
	choices=['insert','select'],); 
    args = parser.parse_args()

    engine = create_engine(SQL_CONNECTION)
    conn = engine.connect( )

    if args.command == "insert":
        print "Script will put 500 new records to database"
        insert_data(conn)
    elif args.command == "select":
        print ("Script will select statistics and write it to: " + DEFAULT_RESULT_FILE)
        write_output(DEFAULT_RESULT_FILE, select_data(conn) )
    else:
        print ("Unknown command: " +args.command)

    conn.close()
