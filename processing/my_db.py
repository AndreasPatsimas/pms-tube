import mysql.connector

def run_sql_command(query, host, port, user, password):
    cnx = mysql.connector.connect(host=host, port=port, user=user, password=password)
    my_cursor = cnx.cursor()
    results = my_cursor.execute(query, multi=True)
    cnx.commit()

    # Do some looping with exception handling
    while True:
        try:
            next(results)
        except Exception as e:
            break

    cnx.close()


def run_insert_command(query, record_tuple, host, port, user, password):
    print("insert data: ", record_tuple)
    cnx = mysql.connector.connect(host=host, port= port, user=user, password=password, database='test')
    my_cursor = cnx.cursor()
    results = my_cursor.execute(query, record_tuple)
    cnx.commit()

    while True:
        try:
            next(results)
        except Exception as e:
            break

    cnx.close()

def get_videos(host, port, user, password):
    cnx = mysql.connector.connect(host=host, port= port, user=user, password=password, database='test')
    mycursor = cnx.cursor()
    mycursor.execute('select * from videos')
    results = mycursor.fetchall()
    cnx.commit()
    cnx.close()
    return results

def get_stats_from_video(host, port, user, password, video_id):
    cnx = mysql.connector.connect(host=host, port= port, user=user, password=password, database='test')
    mycursor = cnx.cursor()
    mycursor.execute('select views, likes, dislikes from stats where video_id = ' + str(video_id))
    results = mycursor.fetchall()
    cnx.commit()
    cnx.close()
    return results