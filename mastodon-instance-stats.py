import argparse
import requests
import json
import sys

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
    parser = argparse.ArgumentParser(prog="Mastodon Instance Stats", description="Fetches instance global stats and optionally saves it")
    parser.add_argument('instances', metavar="INSTANCE", type=str, nargs="+", help="instance(s) to show stats for")
    args = parser.parse_args()

    print('=============== Mastodon instance stats ===============')

    instances_data = {}
    for instance in args.instances:
        instance_data = getDataOfInstance(instance)
        instances_data[instance] = {
            'title': instance_data['title'],
            'user_count': instance_data['stats']['user_count'],
            'status_count': instance_data['stats']['status_count'],
            'domain_count': instance_data['stats']['domain_count']
        }

        data = instances_data[instance]
        printStatsOfSingleInstance(data['title'], data['user_count'], data['status_count'], data['domain_count'])

    # Printing the whole Mastodon instance stats
    if len(instances_data) == 2:
        data_left = instances_data[args.instances[0]]
        data_right = instances_data[args.instances[1]]

        print('=== Comparisons ===')
        printComparisons('Users', data_left['title'], data_right['title'], data_left['user_count'], data_right['user_count'])
        printComparisons('Toots', data_left['title'], data_right['title'], data_left['status_count'], data_right['status_count'])
        printComparisons('Connections', data_left['title'], data_right['title'], data_left['domain_count'], data_right['domain_count'])

if __name__ == "__main__":
    main()
