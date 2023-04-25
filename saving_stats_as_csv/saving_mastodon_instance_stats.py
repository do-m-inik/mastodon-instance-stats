import requests
import json
import sys
import csv
import os
from datetime import datetime

# Printing the usage of the program if is was typed incorrectly
def printInvalidSyntaxError():
    print('Usage: python3 saving_mastodon_instance_stats.py')
    print('Example: python3 saving_mastodon_instance_stats.py bahn.social')
    sys.exit(1)

# Getting the URL with the name of a instance
def getURLOfInstance(name):
    return 'https://' + name + '/api/v1/instance'

# If a invalid URL was given this function returns the error for it
def checkIfMastodonInstanceExists(name):
    try:
        r = requests.head(getURLOfInstance(name))
    except:
        print('Your given URL is not a Mastodon instance!')
        print('Not working URL: https://' + name)
        sys.exit(1)

# Getting the response of a Mastodon instance
def getResponseOfInstance(url):
    return requests.get(url)

# Getting the data of the instance given by JSON located in instance_name.domain/api/v1/instance
def getDataOfInstance(name):
    checkIfMastodonInstanceExists(name)
    url = getURLOfInstance(name)
    response = getResponseOfInstance(url)
    return json.loads(response.text)

def main():
    # Given instance
    argument_count = len(sys.argv)
    if(argument_count != 2):
        printInvalidSyntaxError() # If too less/many arguments are given
    choosen = sys.argv[1] # The choosen instance is the given instance

    # Data of the given instance
    data_choosen = getDataOfInstance(choosen)

    # Single data elements given by the choosen instance
    title_choosen = data_choosen['title']
    user_count_choosen = data_choosen['stats']['user_count']
    status_count_choosen = data_choosen['stats']['status_count']
    domain_count_choosen = data_choosen['stats']['domain_count']

    # CSV part
    now = datetime.now()
    date_and_time = now.strftime("%d.%m.%Y %H:%M:%S") # Saving the current date and time for the CSV
    path = 'mastodon_instance_stats.csv' # Name of the CSV
    data = [date_and_time, title_choosen, user_count_choosen, status_count_choosen, domain_count_choosen] # header line
    if not(os.path.isfile(path)): # If CSV not exist: creating a new CSV
        column_name = ["Date and time", "Instance name", "Users", "Toots", "Connections"]
        with open(path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(column_name)
            writer.writerow(data)
    else:
        with open(path, 'a') as f: # Appending data to existing CSV
            writer = csv.writer(f)
            writer.writerow(data)

if __name__ == "__main__":
    main()
