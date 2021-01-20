from youtubesearchpython import *
from pytube import Playlist
from pytube import YouTube
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from processing.my_db import *
from processing.utils import *
from datetime import datetime
import sys

# start=timer()
# end=timer()
# print(end-start)

def exit():
    print('{} Now the system will exit '.format(datetime.datetime.now())) #this works ok
    sys.exit()

def reset_all(host, port, user, password):
    sql_create = """DROP DATABASE `test`; """
    sql_create1 = """create database if not exists test;use test;CREATE TABLE IF NOT EXISTS `videos` (`id` INT(11) NOT NULL AUTO_INCREMENT,`title` VARCHAR(200) NOT NULL,`link` VARCHAR(75) NOT NULL ,`duration` INT NOT NULL,`p` FLOAT(12) NULL DEFAULT NULL, `r` FLOAT(12) NULL DEFAULT NULL,`LPV` FLOAT(12) NULL DEFAULT NULL,`DPV` FLOAT(12) NULL DEFAULT NULL,`VPD` FLOAT(12) NULL DEFAULT NULL,`ci` FLOAT(12) NULL DEFAULT NULL,PRIMARY KEY (`id`));"""
    sql_create2 = """use test;CREATE TABLE IF NOT EXISTS `stats` (`id` INT(11) NOT NULL AUTO_INCREMENT,`views` INT(11) NULL DEFAULT NULL,`likes` INT(11) NULL DEFAULT NULL,`dislikes` INT(11) NULL DEFAULT NULL, `last_inserted` DATETIME NOT NULL, `video_id` INT(11) NOT NULL, PRIMARY KEY (`id`), FOREIGN KEY (video_id) REFERENCES videos(id));"""

    run_sql_command(sql_create, host, port, user, password)
    run_sql_command(sql_create1, host, port, user, password)
    run_sql_command(sql_create2, host, port, user, password)

def save_videos(host, port, user, password):
    total = 0
    counter = 0
    playlist_count = 0
    video_insertion_count = 0
    playlist_insertion_count = 0
    overall_playlist_length = 0
    x = input('Give cartoon series ')
    word = x.split()
    y = "cartoon english subtitles"

    allSearch = Search(x + y, limit=4)
    result2 = allSearch.result()

    result3 = result2.get('result')
    length = len(result3)
    print("result3:", result3)
    for j in range(0, length):
        if result3[j]['type'] == 'video':
            duration = result3[j]['duration']

            total = total + get_duration(duration)
            counter = counter + 1

    average_duration = total / counter

    for i in range(0, length):
        if result3[i]['type'] == 'video' and video_insertion_count <= 100:
            acknowledged = False
            for w in word:
                if w.upper() in result3[i]['title'].upper() and acknowledged == False:

                    if (get_duration(result3[i]['duration']) <= 1.2 * average_duration and "Compilation" not in
                            result3[i][
                                'title'] and "Episodes" not in result3[i]['title'] and eval_subtitles(
                                result3[i]['id']) == True):
                        video_insertion_count = video_insertion_count + 1
                        tup = (result3[i]['title'], result3[i]['link'], get_duration(result3[i]['duration']))
                        run_insert_command('insert into videos (title,link,duration) values (%s,%s,%s)', tup, host,
                                           port, user, password)
                        acknowledged = True

        elif result3[i]['type'] == 'playlist':

            playlist_count = playlist_count + 1
            if playlist_count < 3:
                playlist = Playlist(result3[i]['link'])
                pl = playlist.video_urls
                for vid in pl:
                    le = YouTube(vid).length
                    overall_playlist_length = overall_playlist_length + le
                average_playlist_video_length = overall_playlist_length / len(pl)
                for vid in pl:
                    title = YouTube(vid).title
                    acknowledged = False
                    for w in word:
                        if x.upper() in title.upper() and playlist_insertion_count <= 300 and acknowledged == False and YouTube(
                                vid).length <= 1.2 * average_playlist_video_length and "Compilation" not in YouTube(
                            vid).title and "Episodes" not in YouTube(vid).title and eval_subtitles(
                            strip_link(vid)) == True:
                            playlist_insertion_count = playlist_insertion_count + 1
                            tup = (title, vid, YouTube(vid).length)

                            run_insert_command("insert into videos (title,link,duration) values (%s,%s,%s)", tup, host,
                                               port, user, password)

                            acknowledged = True

def save_stats(host, port, user, password):
    videos = get_videos(host, port, user, password)
    for video in videos:
        id = video[0]
        link = video[2]
        data = get_video_info(link)
        tup = (data['views'], data['likes'], data['dislikes'], datetime.now(), id)
        run_insert_command('insert into stats (views, likes, dislikes, last_inserted, video_id) values (%s,%s,%s,%s,%s)',
                           tup, host, port, user, password)

def save_indicators(host, port, user, password):

    videos = get_videos(host, port, user, password)

    for video in videos:

        video_id = video[0]

        preferences = get_avg_stats_likes_and_dislikes(host, port, user, password, video_id)
        avg_likes = preferences[0][0]
        avg_dislikes = preferences[0][1]
        p = avg_likes / avg_dislikes

        stats = get_min_max_values_stats(host, port, user, password, video_id)
        max_views = stats[0][0]
        min_views = stats[0][1]
        max_likes = stats[0][2]
        min_likes = stats[0][3]
        max_dislikes = stats[0][4]
        min_dislikes = stats[0][5]


        r = 183 * (max_views - min_views) / max_views
        LPV = (max_likes - min_likes) / (max_views - min_views)
        DPV = (max_dislikes - min_dislikes) / (max_views - min_views)
        VPD = (max_views - min_views) / 2

        youtube_video_link = strip_link(video[2])
        s = strip_subs(youtube_video_link)
        blob = TextBlob(s)
        blob2 = TextBlob(s, analyzer=NaiveBayesAnalyzer())
        transform = transformPA(blob.sentiment[0])
        ci = (max(blob2.sentiment[1], blob2.sentiment[2]) + transform) / 2

        update_videos(host, port, user, password, p, r, LPV, DPV, VPD, ci, video_id)



def sentiment_analysis(host, port, user, password):

    # sklearn.preprocessing.normalize(X, norm='l2', *, axis=1, copy=True, return_norm=False)
    # X--> dataframe
    videos = get_videos(host, port, user, password)
    print("sentiment analysis")

    # sysxetish ->
    # https://machinelearningmastery.com/how-to-use-correlation-to-understand-the-relationship-between-variables/#:~:text=The%20Pearson%20correlation%20coefficient%20(named,deviation%20of%20each%20data%20sample