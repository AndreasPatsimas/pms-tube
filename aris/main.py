from youtubesearchpython import *
from pytube import Playlist
from pytube import YouTube
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from processing.my_db import run_sql_command, run_insert_command, get_video_links
from processing.utils import *

sql_create1 = """create database if not exists test;use test;CREATE TABLE IF NOT EXISTS `videos` (`id` INT(11) NOT NULL AUTO_INCREMENT,`title` VARCHAR(200) NOT NULL,`link` VARCHAR(75) NOT NULL ,`duration` INT NOT NULL,`composite_index` FLOAT(12) NULL DEFAULT NULL,PRIMARY KEY (`id`));"""
sql_create2 = """use test;CREATE TABLE IF NOT EXISTS `stats` (`id` INT(11) NOT NULL AUTO_INCREMENT,`views` INT(11) NULL DEFAULT NULL,`likes` INT(11) NULL DEFAULT NULL,`dislikes` INT(11) NULL DEFAULT NULL,PRIMARY KEY (`id`));"""

# host = input("Give ip/host:")
# port = input("Give port:")
# user = input("Give username:")
# password = input("Give password:")
host = 'localhost'
port = '3306'
user = 'root'
password = '19141918'

total = 0
counter = 0
playlist_count = 0
video_insertion_count = 0
playlist_insertion_count = 0
average_duration = 0
total_count = 0
overall_playlist_length = 0
average_playlist_video_length = 0
y = "cartoon english subtitles"
x = input('Give cartoon series ')
word = x.split()

run_sql_command(sql_create1, host, port, user, password)
run_sql_command(sql_create2, host, port, user, password)

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

                if (get_duration(result3[i]['duration']) <= 1.2 * average_duration and "Compilation" not in result3[i][
                    'title'] and "Episodes" not in result3[i]['title'] and eval_subtitles(result3[i]['id']) == True):
                    video_insertion_count = video_insertion_count + 1
                    tup = (result3[i]['title'], result3[i]['link'], get_duration(result3[i]['duration']))
                    run_insert_command('insert into videos (title,link,duration) values (%s,%s,%s)', tup, host, port, user, password)
                    data = get_video_info(str(result3[i]['link']))

                    tup = (data['views'], data['likes'], data['dislikes'], result3[i]['id'])
                    run_insert_command('insert into stats (views, likes, dislikes) values (%s,%s,%s)', tup, host,
                                       port, user, password)
                    # get_views(result3[i]['viewCount']['text'])
                    acknowledged = True
    elif result3[i]['type'] == 'playlist':

        playlist_count = playlist_count + 1
        if playlist_count < 4:
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
                            strip_id(vid)) == True:
                        playlist_insertion_count = playlist_insertion_count + 1
                        tup = (title, vid, YouTube(vid).length)

                        run_insert_command("insert into videos (title,link,duration) values (%s,%s,%s)", tup, host, port, user, password)
                        data = get_video_info(str(result3[i]['link']))
                        tup = (data['views'], data['likes'], data['dislikes'])
                        run_insert_command('insert into stats (views, likes, dislikes) values (%s,%s,%s)',
                                           tup, host,
                                           port, user, password)
                        acknowledged = True

print("average_duration:", average_duration)
print("video_insertion_count:", video_insertion_count)
print("playlist_insertion_count:", playlist_insertion_count)

my_result = get_video_links(host, port, user, password)

print("video links:", my_result)

l = len(my_result)
for item in my_result:
    ide = strip_id(list(item)[0])
    s = strip_subs(ide)
    blob = TextBlob(s)
    blob2 = TextBlob(s, analyzer=NaiveBayesAnalyzer())
    #composite_index=
    print(blob.sentiment)
    print(blob2.sentiment)