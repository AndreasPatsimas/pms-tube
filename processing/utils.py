import re
from youtube_transcript_api import YouTubeTranscriptApi
from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs

# init session
session = HTMLSession()

def get_duration(dur1):
    dur = dur1.split(':')
    mins = dur[0]
    secs = dur[1]
    total_secs = int(mins) * 60 + int(secs)
    return total_secs


def eval_subtitles(id1):
    boo = False
    c = 0
    try:
        t = YouTubeTranscriptApi.get_transcript(id1, languages=['en'])
        l = len(t)
        if l == 0:
            boo = False
        else:
            for z in range(0, l):
                if t[z]['duration'] > 3.5:
                    c = c + 1
                    if c < 3:
                        boo = True
                    else:
                        boo = False
    except:
        boo = False
    return boo


def strip_link(url):
    pos = url.find('=')
    id1 = url[pos + 1:len(url)]
    return (id1)


def get_views(viewcount):
    vc = viewcount.replace('views', '')
    return vc

def strip_subs(id1):
    subs = ''
    t = YouTubeTranscriptApi.get_transcript(id1, languages=['en'])
    for k in range(0, len(t)):
        subs = subs + t[k]['text']
    subtitles = re.sub(r'\(.*?\)', '', subs)
    subtitles = re.sub(r'\[.*?\]', '', subtitles)
    return subtitles

def transformPA(pol):
    trans = (pol + 1)/2
    return trans

def get_video_info(url):
    print("stats from url: ", url)
    # download HTML code
    response = session.get(url)
    # execute Javascript
    response.html.render(sleep=1, timeout= 100.0)
    soup = bs(response.html.html, "html.parser")
    result = {}

    # video views (converted to integer)
    result["views"] = int(''.join([ c for c in soup.find("span", attrs={"class": "view-count"}).text if c.isdigit() ]))

    # number of likes
    text_yt_formatted_strings = soup.find_all("yt-formatted-string", {"id": "text", "class": "ytd-toggle-button-renderer"})
    result["likes"] = int(''.join([ c for c in text_yt_formatted_strings[0].attrs.get("aria-label") if c.isdigit() ]))
    # number of dislikes
    result["dislikes"] = int(''.join([ c for c in text_yt_formatted_strings[1].attrs.get("aria-label") if c.isdigit() ]))

    return result