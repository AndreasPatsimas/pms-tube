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

def update_videos(host, port, user, password, p, r, LPV, DPV, VPD, ci, video_id):

    cnx = mysql.connector.connect(host=host, port= port, user=user, password=password, database='test')
    my_cursor = cnx.cursor()
    results = my_cursor.execute("update test.videos set p = " + str(p) + ", r = " + str(r) + ", LPV = " + str(LPV) + ", DPV = "
                                + str(DPV) + ", VPD = " + str(VPD) + ", ci = " + str(ci) + " "
                                "where id = " + str(video_id))
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

def get_top_three_video_ids(host, port, user, password):
    cnx = mysql.connector.connect(host=host, port= port, user=user, password=password, database='test')
    mycursor = cnx.cursor()
    mycursor.execute('Select id from test.videos order by ci DESC LIMIT 3')
    results = mycursor.fetchall()
    cnx.commit()
    cnx.close()
    return results

def get_bottom_three_video_ids(host, port, user, password):
    cnx = mysql.connector.connect(host=host, port= port, user=user, password=password, database='test')
    mycursor = cnx.cursor()
    mycursor.execute('Select id from test.videos order by ci ASC LIMIT 3')
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

def get_avg_stats_likes_and_dislikes(host, port, user, password, video_id):
    cnx = mysql.connector.connect(host=host, port= port, user=user, password=password, database='test')
    mycursor = cnx.cursor()
    mycursor.execute('SELECT avg(likes), avg(dislikes) FROM stats where video_id = ' + str(video_id))
    results = mycursor.fetchall()
    cnx.commit()
    cnx.close()
    return results

def get_min_max_values_stats(host, port, user, password, video_id):
    cnx = mysql.connector.connect(host=host, port= port, user=user, password=password, database='test')
    mycursor = cnx.cursor()
    mycursor.execute('SELECT max(views), min(views), max(likes), min(likes), max(dislikes), min(dislikes) '
                     'FROM test.stats where video_id = ' + str(video_id))
    results = mycursor.fetchall()
    cnx.commit()
    cnx.close()
    return results