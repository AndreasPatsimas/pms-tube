# from youtube_search import YoutubeSearch
# from youtube_transcript_api import YouTubeTranscriptApi
#
# # pip install numpy==1.19.3
#
# results = YoutubeSearch('Έτερος Εγώ (official full movie)', max_results=10).to_dict()
#
# print(results)
#
# subs = YouTubeTranscriptApi.get_transcript(results[0].get("id"))
#
# print(subs)
#
# # https://pypi.org/project/youtube-search-python/

from datetime import datetime

# datetime object containing current date and time
now = datetime.now()

print("now =", now)
print(type(now))

# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("date and time =", dt_string)


def print_headers():
    print("+-------------------------------+")
    print("|      Welcome to our           |")
    print("|      PMS-TUBE's Menu         |")
    print("+-------------------------------+")


def print_menu():
    print("Please make a selection...")
    print("1) Reset all results and save videos from scratch")
    print("2) Save stats for every video")
    print("3) Sentimental Analysis")
    print("4) Exit")


def get_input():
    choice = 0
    while (choice < 1 or choice > 4) :
        try:
            choice = int(input())
        except:
            print("Invalid choice...")

        if (choice < 1 or choice > 4):
            print("Make the right choice...")

    return choice

def make_choice(choice):
    if(choice == 1):
        print("1")
    elif(choice == 2):
        print("2")
    elif(choice == 3):
        print("3")
    elif(choice == 4):
        print("Thank you for using PMS-TUBE's application")
        return True

    return False

def run_menu():
    print_headers()
    exit = False
    while (not exit):
        print_menu()
        choice = get_input()
        exit = make_choice(choice)
