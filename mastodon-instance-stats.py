import requests
import json
import sys

# Printing the usage of the program if is was typed incorrectly
def printInvalidSyntaxError():
    print('Usage: python3 mastodon-instance-stats.py <choosen instance> [<compared instance>]')
    print('Example 1: python3 mastodon-instance-stats.py bahn.social')
    print('Example 2: python3 mastodon-instance-stats.py bahn.social chaos.social')
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

# Printing the stats of a single Mastodon instance
def printStatsOfSingleInstance(title, user_count, status_count, domain_count):
    print('=== ' + title + ' ===')
    print('Users:', user_count)
    print('Toots:', status_count)
    print('Connections:', domain_count)
    print('')

# Calculating the positive difference of to given values
def calcDifference(count_choosen, count_compared):
    difference = count_compared-count_choosen
    if(difference < 0):
        difference = difference * (-1)
    return difference

# Calculating the ratio of two given Mastodon instances in percent
def calcRatio(count_choosen, count_compared):
    return round(count_choosen/count_compared*100, 2)

# Calculating how many people from the 1st given instance would fit in the 2nd given instance
def calcHowManyPer(count_choosen, count_compared):
    return round(count_compared/count_choosen, 2)

# Printing every comparisation between the two instances
def printComparisons(type, title_choosen, title_compared, count_choosen, count_compared):
    print('= ' + type + ' =')
    print('Difference:', calcDifference(count_choosen, count_compared))
    print('Ratio ' + title_choosen + '/' + title_compared + ':', calcRatio(count_choosen, count_compared), '%')
    print('How many ' + title_compared + ' ' + type.lower() + ' per ' + title_choosen + ' ' + type.lower() + ':',
            calcHowManyPer(count_choosen, count_compared))
    print('')

def main():
    # Given instance/s
    argument_count = len(sys.argv)
    if(argument_count < 2 or argument_count > 3):
        printInvalidSyntaxError() # If too less/many arguments are given
    choosen = sys.argv[1] # The choosen instance is the 1st given instance
    if(argument_count == 3):
        compared = sys.argv[2] # The compared instance is the 2nd given instance

    # Data of the given instance/s
    data_choosen = getDataOfInstance(choosen)
    if(argument_count == 3):
        data_compared = getDataOfInstance(compared)

    # Single data elements given by the choosen instance
    title_choosen = data_choosen['title']
    user_count_choosen = data_choosen['stats']['user_count']
    status_count_choosen = data_choosen['stats']['status_count']
    domain_count_choosen = data_choosen['stats']['domain_count']

    # Single data elements given by the 2nd given instance
    if(argument_count == 3):
        title_compared = data_compared['title']
        user_count_compared = data_compared['stats']['user_count']
        status_count_compared = data_compared['stats']['status_count']
        domain_count_compared = data_compared['stats']['domain_count']

    # Printing the whole Mastodon instance stats
    print('=============== Mastodon instance stats ===============')
    printStatsOfSingleInstance(title_choosen, user_count_choosen, status_count_choosen, domain_count_choosen)
    if(argument_count == 3):
        printStatsOfSingleInstance(title_compared, user_count_compared, status_count_compared, domain_count_compared)
        print('=== Comparisons ===')
        printComparisons('Users', title_choosen, title_compared, user_count_choosen, user_count_compared)
        printComparisons('Toots', title_choosen, title_compared, status_count_choosen, status_count_compared)
        printComparisons('Connections', title_choosen, title_compared, domain_count_choosen, domain_count_compared)

if __name__ == "__main__":
    main()
