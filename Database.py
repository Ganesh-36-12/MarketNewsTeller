import sqlite3 as sq

def get_connection():
  conn = sq.connect('info_collector.db')
  cursor = conn.cursor()
  return conn,cursor
  
try:
  conn,cursor = get_connection()
  create_command_1 = """
  CREATE TABLE IF NOT EXISTS
  SCRAPED (NEWS STRING NOT NULL);
  """
  cursor.execute(create_command_1)

  create_command_2 = """
  CREATE TABLE IF NOT EXISTS
  meta_data (message_id integer not null,
  group_id integer not null
  );
  """
  cursor.execute(create_command_2)

  create_command_3 = """
  CREATE TABLE IF NOT EXISTS
  last_id (message_id integer not null
  );
  """
  cursor.execute(create_command_3)

  create_command_4 = """
  CREATE TABLE IF NOT EXISTS
  BS_SCRAPED (news string not null);
  """
  cursor.execute(create_command_4)
except Exception as e:
  print(e)
finally:
  cursor.close()
  conn.close()

def fetch_old_news(table_name):
  try:
    conn,cursor = get_connection()
    fetch_command = f" SELECT NEWS FROM {table_name} ORDER BY ROWID DESC LIMIT 1 "
    records=cursor.execute(fetch_command).fetchone()
    if len(records)!=0:
      old_news = records[0]
      return old_news
    else:
      return " "
  except Exception as e:
      print("From fetch old news",e)
      return " "
  finally:
    cursor.close()
    conn.close()

def insert_data_into_db(table_name,data_list):
  try:
    conn,cursor = get_connection()
    insert_command = ""
    if table_name.lower() == "meta_data":
      insert_command = f"INSERT INTO {table_name} (message_id,group_id) VALUES(?,?);"
      data = tuple(data_list)
    elif table_name.lower() == "last_id":
      insert_command = f"INSERT INTO {table_name} (message_id) VALUES(?);"
      data = (data_list[0],)
    elif table_name.lower() == "scraped" or table_name.lower() == "bs_scraped":
      insert_command = f"INSERT INTO {table_name} (NEWS) VALUES(?);"
      if data_list[0].startswith("Stock Market LIVE Updates:"):
        data = (data_list[1],)
      else:
        data = (data_list[0],)
    cursor.execute(insert_command,data)
    conn.commit()
  except Exception as e:
      print("From fetch old news",e)
      return " "
  finally:
    cursor.close()
    conn.close()  
      
def fetch_last_id(table_name):
  '''
  INPUT : name of the table
  OUTPUT: returns last msg_id of thr table
  '''  
  try:
    conn,cursor = get_connection()
    fetch_command_1 = f"SELECT message_id FROM {table_name} ORDER BY rowid DESC LIMIT 1;"
    cursor.execute(fetch_command_1)
    record = cursor.fetchone()
    return record
  except Exception as e:
    print(e)
  finally:
    cursor.close()
    conn.close()  

def fetch_all_id(id):
  '''
  INPUT : start msg_id
  OUTPUT: list of msg_ids
  '''  
  try:
    conn,cursor = get_connection()
    fetch_command_2 = f"Select message_id from meta_data where rowid > {id} and group_id = -1002183045099"
    cursor.execute(fetch_command_2)
    records = cursor.fetchall()
    list1 =[x[0] for x in records]
    return list1
  except Exception as e:
    print(e)
  finally:
    cursor.close()
    conn.close()  
    
def final_commit():
  '''
  Updates the last msg_id in the last_id table
  '''
  try:
    conn,cursor = get_connection()
    table2_insert = """ INSERT INTO LAST_ID (MESSAGE_ID) VALUES (?)"""
    msg_id = fetch_last_id("meta_data")
    cursor.execute(table2_insert,msg_id)
    conn.commit()
    print("values are inserted")
  except Exception as e:
    print(e)
  finally:
    cursor.close()
    conn.close()  
