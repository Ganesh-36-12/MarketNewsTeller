import sqlite3 as sq

def create_tables():
  '''
  Create two tables named
      meta_data
      last_id
  '''
  try:
    conn = sq.connect('Meta.db')
    cursor = conn.cursor()
    create_command_1 = """
    CREATE TABLE IF NOT EXISTS 
    meta_data (message_id integer not null,
    group_id integer not null
    );
    """
    cursor.execute(create_command_1)
    create_command_2 = """
    CREATE TABLE IF NOT EXISTS 
    last_id (message_id integer not null
    );
    """
    cursor.execute(create_command_2)
except Exception as e:
    print(e)

def insert_data_into_db(tuple):
  '''
  INPUT : tuple of msg_id and group_id
  TABLE : meta_data
  '''
  try:
    insert_command = """
    INSERT INTO meta_data (message_id,group_id) VALUES(?,?);
    """
    data = (tuple[0],tuple[1])
    cursor.execute(insert_command,data)
    conn.commit()
  except Exception as e:
    print(e)

def fetch_last_id(table_name):
  '''
  INPUT : name of the table
  OUTPUT: returns last msg_id of thr table
  '''  
  try:
    fetch_command_1 = f"SELECT message_id FROM {table_name} ORDER BY rowid DESC LIMIT 1;"
    cursor.execute(fetch_command_1)
    record = cursor.fetchone()
    return record
  except Exception as e:
    print(e)

def fetch_all_id(id):
  '''
  INPUT : msg_id
  OUTPUT: list of msg_ids
  '''  
  try:
    fetch_command_2 = f"Select message_id from meta_data where message_id > {id}"
    cursor.execute(fetch_command_2)
    records = cursor.fetchall()
    list1 =[x[0] for x in records]
    return list1
  except Exception as e:
    print(e)
    
def final_commit():
  '''
  Updates the last msg_id in the last_id table
  '''
  try:
    table2_insert = """ INSERT INTO LAST_ID (MESSAGE_ID) VALUES (?)"""
    msg_id = fetch_last_id("meta_data")
    cursor.execute(table2_insert,msg_id)
    conn.commit()
    print("values are inserted")
  except Exception as e:
    print(e)
