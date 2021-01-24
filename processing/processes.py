from youtubesearchpython import *
from pytube import Playlist
from pytube import YouTube
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from processing.my_db import *
from processing.utils import *
from datetime import datetime
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

# drop tables and recreate
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
        # filtering videos
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

        # filtering playlist and save every video
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

# save stats for every video
def save_stats(host, port, user, password):

    videos = get_videos(host, port, user, password)
    for video in videos:
        id = video[0]
        link = video[2]
        data = get_video_info(link)
        tup = (data['views'], data['likes'], data['dislikes'], datetime.now(), id)
        run_insert_command('insert into stats (views, likes, dislikes, last_inserted, video_id) values (%s,%s,%s,%s,%s)',
                           tup, host, port, user, password)

# save and update indicators p, r, LPV, DPV,VPD, ci
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

    credentials = "mysql://" + user + ":" + password + "@" + host + ":"+ port + "/test"
    # pip install Flask - SQLAlchemy

    # videos with top 3 ci
    video_ids_ci_top_three = get_top_three_video_ids(host, port, user, password)
    video_ids_ci_top_three = video_ids_ci_top_three[0] + video_ids_ci_top_three[1] + video_ids_ci_top_three[2]
    df_ci_stats_top_three = pd.read_sql(" select views, likes, dislikes, last_inserted from stats where video_id in " + str(video_ids_ci_top_three), con=credentials)
    print(df_ci_stats_top_three)

    # videos with bottom 3 ci
    video_ids_ci_bottom_three = get_bottom_three_video_ids(host, port, user, password)
    video_ids_ci_bottom_three = video_ids_ci_bottom_three[0] + video_ids_ci_bottom_three[1] + video_ids_ci_bottom_three[2]
    df_ci_stats_bottom_three = pd.read_sql(" select views, likes, dislikes, last_inserted from stats where video_id in " + str(video_ids_ci_bottom_three), con=credentials)
    print(df_ci_stats_bottom_three)

    df_videos = pd.read_sql("select duration, p, r, LPV, DPV, VPD, ci from videos", con=credentials)

    # correlation between indicators
    corrMatrix = df_videos.corr()

    print(corrMatrix.head())
    plt.figure(figsize=(30, 20))
    sns.clustermap(corrMatrix, annot=True, fmt=".2f")
    plt.show()

    # graphs for videos with top 3 ci and bottom 3 ci
    df_ci_stats_top_three.plot.bar(x="last_inserted", y="views", rot=70, title="Top 3")
    plt.xticks(fontsize=5)
    plt.show(block=True)

    df_ci_stats_top_three.plot.bar(x="last_inserted", y="likes", rot=70, title="Top 3")
    plt.xticks(fontsize=5)
    plt.show(block=True)

    df_ci_stats_top_three.plot.bar(x="last_inserted", y="dislikes", rot=70, title="Top 3")
    plt.xticks(fontsize=5)
    plt.show(block=True)

    df_ci_stats_bottom_three.plot.bar(x="last_inserted", y="views", rot=70, title="Bottom 3")
    plt.xticks(fontsize=5)
    plt.show(block=True)

    df_ci_stats_bottom_three.plot.bar(x="last_inserted", y="likes", rot=70, title="Bottom 3")
    plt.xticks(fontsize=5)
    plt.show(block=True)

    df_ci_stats_bottom_three.plot.bar(x="last_inserted", y="dislikes", rot=70, title="Bottom 3")
    plt.xticks(fontsize=5)
    plt.show(block=True)

    # Display
    # the
    # ranking
    # order
    # of
    # the
    # different
    # cartoons(
    # for the first
    # 150) based on the normalized total number of views
    df_videos_rank = pd.read_sql("SELECT SUBSTRING(title, 1, 15) as title, max(views) as views FROM test.videos v "
                                 "inner join test.stats s on v.id = s.video_id "
                                 "group by title order by s.views desc", con=credentials)

    print(df_videos_rank)
    df_videos_rank.plot.bar(x="title", y="views", rot=70, title="Videos Rankings By Views")
    plt.show(block=True)