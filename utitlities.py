from connection_cred import USER, PASSWORD, HOST, DATABASE
import mysql.connector as ms
from decimal import Decimal
import re
import threading

def DBUpdate(table, field, value):
    cnx = ms.connect(user=USER, password=PASSWORD, host=DATABASE, database=HOST)
    cursor = cnx.cursor()
    query = f"UPDATE `{table}` SET `{field}` = '{value}'"
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()


def DBUpdateARG(table, field, value1, arguement, value2):
    cnx = ms.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cursor = cnx.cursor()
    query = "UPDATE `{}` SET `{}` = '{}' WHERE `{}` = '{}';".format(table,field,value1,arguement,value2)
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()


def DBRead(table, field):
    cnx = ms.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cursor = cnx.cursor(buffered=True)
    query = f"SELECT `{field}` FROM `{table}`"
    cursor.execute(query)
    data = cursor.fetchone()[0]
    cursor.close()
    cnx.close()
    return data


def DBReadARG(table, field, arguement, value, result):
    cnx = ms.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cursor = cnx.cursor(buffered=True)
    query = f"SELECT `{field}` FROM `{table}` WHERE `{arguement}` = '{value}'"
    cursor.execute(query)
    data = cursor.fetchone()[0]
    result[field] = data
    cursor.close()
    cnx.close()
    return data



def custom_round(num, digits=2, Isstr=False):
    tmp = Decimal(num)
    x = ("{0:.%sf}" % digits).format(round(tmp, digits))
    if Isstr:
        return x
    return float(Decimal(x))



def count_words(text):
    # Use regular expression to extract complete words
    words = re.findall(r'\b\w+\b', text)
    
    # Count the number of complete words
    word_count = len(words)
    
    # Return the word count
    return int(word_count)


# result = {}
# minutes_total_task = threading.Thread(target=DBReadARG,args=('user','minutes_total','email','ger@dataspeed.nl',result))
# minutes_count_task = threading.Thread(target=DBReadARG,args=('user','minutes_count','email','ger@dataspeed.nl',result))
# WhisperAIText = DBRead('whisper_config', 'whisper_text')

# minutes_total_task.start()
# minutes_count_task.start()

# minutes_total_task.join()
# minutes_count_task.join()


# # Minutes Usage
# minutes_total = result['minutes_total']
# minutes_count = result['minutes_count']
# print(minutes_total)
# print(minutes_count)
# print(WhisperAIText)