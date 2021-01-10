from youtube_search import YoutubeSearch
from youtube_transcript_api import YouTubeTranscriptApi

# pip install numpy==1.19.3

results = YoutubeSearch('Έτερος Εγώ (official full movie)', max_results=10).to_dict()

print(results)

subs = YouTubeTranscriptApi.get_transcript(results[0].get("id"))

print(subs)

# https://pypi.org/project/youtube-search-python/