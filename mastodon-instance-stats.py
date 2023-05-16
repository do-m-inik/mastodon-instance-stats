import argparse
import csv
import datetime
import json
import os
import shutil
import sys
import tempfile

import requests

CSV_COLUMNS = ["Date and time", "Instance name", "Domain", "Users", "Toots", "Connections", "DUsers", "DToots", "DConnections"]

def getURLOfInstance(name):
    """Getting the URL with the name of a instance"""

    return 'https://' + name + '/api/v1/instance'


def checkIfMastodonInstanceExists(name):
    """If a invalid URL was given this function returns the error for it"""

    try:
        r = requests.head(getURLOfInstance(name))
    except:
        print('Your given URL is not a Mastodon instance!')
        print('Not working URL: https://' + name)
        sys.exit(1)


def getResponseOfInstance(url):
    """Getting the response of a Mastodon instance"""

    return requests.get(url)


def getDataOfInstance(name):
    """Getting the data of the instance given by JSON located in instance_name.domain/api/v1/instance"""

    checkIfMastodonInstanceExists(name)
    url = getURLOfInstance(name)
    response = getResponseOfInstance(url)
    return json.loads(response.text)


def printStatsOfSingleInstance(title, user_count, status_count, domain_count):
    """Printing the stats of a single Mastodon instance"""

    print('=== ' + title + ' ===')
    print('Users:', user_count)
    print('Toots:', status_count)
    print('Connections:', domain_count)
    print('')


def calcDifference(count_choosen, count_compared):
    """Calculating the positive difference of to given values"""

    difference = count_compared-count_choosen
    if(difference < 0):
        difference = difference * (-1)
    return difference


def calcRatio(count_choosen, count_compared):
    """Calculating the ratio of two given Mastodon instances in percent"""

    return round(count_choosen/count_compared*100, 2)


def calcHowManyPer(count_choosen, count_compared):
    """Calculating how many people from the 1st given instance would fit in the 2nd given instance"""

    return round(count_compared/count_choosen, 2)


def printComparisons(type, title_choosen, title_compared, count_choosen, count_compared):
    """Printing every comparisation between the two instances"""

    print('= ' + type + ' =')
    print('Difference:', calcDifference(count_choosen, count_compared))
    print('Ratio ' + title_choosen + '/' + title_compared + ':', calcRatio(count_choosen, count_compared), '%')
    print('How many ' + title_compared + ' ' + type.lower() + ' per ' + title_choosen + ' ' + type.lower()[:-1] + ':',
            calcHowManyPer(count_choosen, count_compared))
    print('')


def migrateCSV(filename):
    """Reads whole csv and adds columns with calculated difference values"""

    output_filehandle, output_filename = tempfile.mkstemp()
    with os.fdopen(output_filehandle, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=CSV_COLUMNS)
        writer.writeheader()

        with open(filename, 'r', newline='', encoding='utf-8') as infile:
            reader = csv.DictReader(infile, CSV_COLUMNS)
            previous_values = {
                'Users': 0,
                'Toots': 0,
                'Connections': 0
            }

            # skip header line
            next(reader)

            for rowno, row in enumerate(reader):
                for field in ['Users', 'Toots', 'Connections']:
                    cur_value = 0
                    try:
                        cur_value = int(row[field])
                    except ValueError:
                        # Silence value error to fix empty values
                        pass
                    row["D" + field] = cur_value - previous_values[field]
                    previous_values[field] = cur_value
                writer.writerow(row)

    shutil.move(output_filename, filename)


def migrateCheckCSV(filename):
    """Checks if the file needs to be migrated to new format"""

    with open(filename, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        headers = reader.fieldnames
        if headers != CSV_COLUMNS:
            print('*** File does not match new format, starting migration')
            migrateCSV(filename)


def writeCSV(instances_data, filename):
    """Creates and appends given data to CSV file"""

    if not os.path.exists(filename):
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
            writer.writeheader()

    current_time = datetime.datetime.utcnow()
    formatted_time = current_time.isoformat("Z")
    previous_values = {
        'Users': 0,
        'Toots': 0,
        'Connections': 0
    }

    migrateCheckCSV(filename)
    with open(filename, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile, fieldnames=CSV_COLUMNS)
        for row in reader:
            for field in ['Users', 'Toots', 'Connections']:
                cur_value = 0
                try:
                    cur_value = int(row[field])
                except ValueError:
                    # Silence value error to fix empty values
                    pass
                previous_values[field] = cur_value

    with open(filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        for domain, data in instances_data.items():
            data_row = {
                "Date and time": formatted_time,
                "Instance name": data['title'],
                "Domain": domain,
                "Users": data['user_count'],
                "Toots": data['status_count'],
                "Connections": data['domain_count'],
                "DUsers": int(data['user_count']) - previous_values['Users'],
                "DToots": int(data['status_count']) - previous_values['Toots'],
                "DConnections": int(data['domain_count']) - previous_values['Connections']

            }
            writer.writerow(data_row)


def main():
    parser = argparse.ArgumentParser(description="Fetches instance global stats and optionally saves it")
    parser.add_argument('instances', metavar="INSTANCE", type=str, nargs="+", help="instance(s) to show stats for")
    parser.add_argument('--csv', metavar="CSVFILE", type=str, help="Creates/Appends to given CSV file instead of writing to terminal")
    args = parser.parse_args()

    instances_data = {}
    for instance in args.instances:
        print('Fetching instance data for %s' % instance)
        instance_data = getDataOfInstance(instance)
        instances_data[instance] = {
            'title': instance_data['title'],
            'user_count': instance_data['stats']['user_count'],
            'status_count': instance_data['stats']['status_count'],
            'domain_count': instance_data['stats']['domain_count']
        }

    if args.csv:
        print('Writing CSV to %s' % args.csv)
        writeCSV(instances_data, args.csv)
        sys.exit(0)

    # Printing the whole Mastodon instance stats
    print('=============== Mastodon instance stats v1.2.2 ===============')
    for instance in args.instances:
        data = instances_data[instance]
        printStatsOfSingleInstance(data['title'], data['user_count'], data['status_count'], data['domain_count'])

    if len(instances_data) == 2:
        data_left = instances_data[args.instances[0]]
        data_right = instances_data[args.instances[1]]

        print('=== Comparisons ===')
        printComparisons('Users', data_left['title'], data_right['title'], data_left['user_count'], data_right['user_count'])
        printComparisons('Toots', data_left['title'], data_right['title'], data_left['status_count'], data_right['status_count'])
        printComparisons('Connections', data_left['title'], data_right['title'], data_left['domain_count'], data_right['domain_count'])

if __name__ == "__main__":
    main()
