def print_headers():
    print("+-------------------------------+")
    print("|      Welcome to our           |")
    print("|      PMS-TUBE's Menu         |")
    print("+-------------------------------+")


def print_menu():
    print("Please make a selection...")
    print("1) Reset all results and create database")
    print("2) Search and save videos")
    print("3) Save stats for every video")
    print("4) Sentiment analysis and save indicators")
    print("5) Indicators Analysis")
    print("6) Exit")


def get_input():
    choice = 0
    while (choice < 1 or choice > 6) :
        try:
            choice = int(input())
        except:
            print("Invalid choice...")

        if (choice < 1 or choice > 6):
            print("Make the right choice...")

    return choice

def make_choice(choice, method_one, method_two, method_three, method_four, method_five, host, port, user, password):
    if(choice == 1):
        method_one(host, port, user, password)
    elif(choice == 2):
        method_two(host, port, user, password)
    elif(choice == 3):
        method_three(host, port, user, password)
    elif(choice == 4):
        method_four(host, port, user, password)
    elif(choice == 5):
        method_five(host, port, user, password)
    elif(choice == 6):
        print("Thank you for using PMS-TUBE's application")
        return True

    return False

def run_menu(method_one, method_two, method_three, method_four, method_five):

    host = 'localhost' #10.0.120.49
    port = '3306'
    user = 'root' #test
    password = '19141918' #12345
    print_headers()
    exit = False
    while (not exit):
        print_menu()
        choice = get_input()
        exit = make_choice(choice, method_one, method_two, method_three, method_four, method_five, host, port, user, password)