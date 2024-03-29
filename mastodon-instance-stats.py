import argparse
import csv
import datetime
import json
import os
import sys
from numpy import genfromtxt
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func, MetaData
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
import requests

CSV_COLUMNS = ["Date and time", "Instance name", "Domain", "Users", "Active users", "Toots", "Connections", "DUsers",
               "DActive users", "DToots", "DConnections"]


class Base(DeclarativeBase):
    pass


class TableRow(Base):
    __tablename__ = 'data'
    date_and_time = Column(DateTime, primary_key=True)
    instance_name = Column(String)
    domain = Column(String)
    users = Column(Integer)
    active_users = Column(Integer)
    toots = Column(Integer)
    connections = Column(Integer)
    d_users = Column(Integer)
    d_active_users = Column(Integer)
    d_toots = Column(Integer)
    d_connections = Column(Integer)


def get_api_v1_of_instance(name):
    """Getting the API v1 URL with the name of an instance"""

    return 'https://' + name + '/api/v1/instance'


def get_api_v2_of_instance(name):
    """Getting the API v2 URL with the name of an instance"""

    return 'https://' + name + '/api/v2/instance'


def check_if_mastodon_instance_exists(name):
    """If an invalid URL was given this function returns the error for it"""

    try:
        r = requests.head(get_api_v1_of_instance(name))
    except:
        print('Your given URL is not a Mastodon instance!')
        print('Not working URL: https://' + name)
        sys.exit(1)


def get_response_of_instance(url):
    """Getting the response of a Mastodon instance"""

    return requests.get(url)


def get_api_v1_data_of_instance(name):
    """Getting the data of the instance given by JSON located in instance_name.domain/api/v1/instance"""

    check_if_mastodon_instance_exists(name)
    api_v1_url = get_api_v1_of_instance(name)
    response = get_response_of_instance(api_v1_url)
    return json.loads(response.text)


def get_api_v2_data_of_instance(name):
    """Getting the data of the instance given by JSON located in instance_name.domain/api/v2/instance"""

    check_if_mastodon_instance_exists(name)
    api_v2_url = get_api_v2_of_instance(name)
    response = get_response_of_instance(api_v2_url)
    return json.loads(response.text)


def calc_difference(count_chosen, count_compared):
    """Calculating the positive difference of to given values"""

    difference = count_compared - count_chosen
    if difference < 0:
        difference = difference * (-1)
    return difference


def calc_ratio(count_chosen, count_compared):
    """Calculating the ratio of two given Mastodon instances in percent"""

    return round(count_chosen / count_compared * 100, 2)


def calc_how_many_per(count_chosen, count_compared):
    """Calculating how many people from the 1st given instance would fit in the 2nd given instance"""

    return round(count_compared / count_chosen, 2)


def print_stats_of_single_instance(title, user_count, status_count, domain_count, active_users):
    """Printing the stats of a single Mastodon instance"""

    print('=== ' + title + ' ===')
    print('Total Users: ', user_count)
    print('Active Users:', active_users)
    print('> Ratio:     ', calc_ratio(active_users, user_count), '%')
    print('Toots:       ', status_count)
    print('Connections: ', domain_count)
    print('')


def print_comparisons(instance_type, title_chosen, title_compared, count_chosen, count_compared):
    """Printing every comparison between the two instances"""

    print('= ' + instance_type + ' =')
    print('Difference:', calc_difference(count_chosen, count_compared))
    print('Ratio ' + title_chosen + '/' + title_compared + ':', calc_ratio(count_chosen, count_compared), '%')
    print('How many ' + title_compared + ' ' + instance_type.lower() + ' per ' + title_chosen + ' ' +
          instance_type.lower()[:-1] + ':', calc_how_many_per(count_chosen, count_compared))
    print('')


def load_csv(file_name):
    with open(file_name, 'r') as file:
        num_columns = len(file.readline().split(','))
    data = genfromtxt(file_name, delimiter=',', skip_header=1, dtype=str, encoding=None, autostrip=True,
                         usecols=range(num_columns))
    return data.tolist()


def write_csv(instances_data, filename):
    """Creates and appends given data to CSV file"""

    if not os.path.exists(filename):
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
            writer.writeheader()

    current_time = datetime.datetime.utcnow()
    formatted_time = current_time.isoformat(" ")
    previous_values = {
        'Users': 0,
        'Active users': 0,
        'Toots': 0,
        'Connections': 0
    }

    with open(filename, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile, fieldnames=CSV_COLUMNS)
        for row in reader:
            for field in ['Users', 'Active users', 'Toots', 'Connections']:
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
                "Active users": data['active_users'],
                "Toots": data['status_count'],
                "Connections": data['domain_count'],
                "DUsers": int(data['user_count']) - previous_values['Users'],
                "DActive users": int(data['active_users']) - previous_values['Active users'],
                "DToots": int(data['status_count']) - previous_values['Toots'],
                "DConnections": int(data['domain_count']) - previous_values['Connections']

            }
            writer.writerow(data_row)


def insert_data_into_database(instances_data, filename):
    """Creates and appends given data to DB file"""

    engine = create_engine("sqlite:///" + filename, echo=True)
    Base.metadata.create_all(engine)
    current_time = datetime.datetime.utcnow()

    with Session(engine) as session:
        # Checking if the given DB file is empty
        row_count = session.query(func.count(TableRow.date_and_time)).scalar()
        if row_count > 0:
            # Getting the data from the last row
            last_row = session.query(TableRow).order_by(TableRow.date_and_time.desc()).first()
            previous_values = {
                'Users': last_row.users,
                'Active_users': last_row.active_users,
                'Toots': last_row.toots,
                'Connections': last_row.connections
            }
        else:
            # If no row exists in the DB the delta values are getting to 0
            previous_values = {
                'Users': 0,
                'Active_users': 0,
                'Toots': 0,
                'Connections': 0
            }

        # Adding for every given instance name the values as a row
        for domain, data in instances_data.items():
            data_row = TableRow(
                date_and_time=current_time,
                instance_name=data['title'],
                domain=domain,
                users=data['user_count'],
                active_users=data['active_users'],
                toots=data['status_count'],
                connections=data['domain_count'],
                d_users=int(data['user_count']) - previous_values['Users'],
                d_active_users=int(data['active_users']) - previous_values['Active_users'],
                d_toots=int(data['status_count']) - previous_values['Toots'],
                d_connections=int(data['domain_count']) - previous_values['Connections'],
            )
            session.add(data_row)

            # Actual data now gets to the previous values
            previous_values['Users'] = data['user_count']
            previous_values['Active_users'] = data['active_users']
            previous_values['Toots'] = data['status_count']
            previous_values['Connections'] = data['domain_count']

        session.commit()


def convert_csv_to_db(csv_name, db_name):
    """Converts a given CSV file to a DB file"""

    engine = create_engine('sqlite:///' + db_name)
    Base.metadata.create_all(engine)
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()
    data = load_csv(csv_name)

    # Commit every row of the CSV into the DB
    for row in data:
        current_date_iso = row[0]
        current_date_iso_string = current_date_iso.strip("b''")
        current_datetime = datetime.datetime.strptime(current_date_iso_string, '%Y-%m-%d %H:%M:%S.%f')
        data_row = TableRow(
            date_and_time=current_datetime,
            instance_name=row[1],
            domain=row[2],
            users=row[3],
            active_users=row[4],
            toots=row[5],
            connections=row[6],
            d_users=row[7],
            d_active_users=row[8],
            d_toots=row[9],
            d_connections=row[10],
        )
        s.add(data_row)
    s.commit()


def convert_db_to_csv(db_name, csv_name):
    """Converts a given DB file to a CSV file"""

    engine = create_engine('sqlite:///' + db_name)
    connection = engine.connect()
    metadata = MetaData()
    metadata.reflect(bind=engine)

    # Getting the data of the only table in the DB
    table = metadata.tables['data']
    query = table.select()
    result = connection.execute(query)
    rows = result.fetchall()
    column_names = table.columns.keys()

    # Open the CSV and writing into it
    with open(csv_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(column_names)
        for row in rows:
            writer.writerow(row)

    connection.close()


def main():
    parser = argparse.ArgumentParser(description="Fetches instance global stats and optionally saves it")
    parser.add_argument('instances', metavar="INSTANCE", type=str, nargs="*", help="instance(s) to show stats for")
    parser.add_argument('--csv', metavar="CSVFILE", type=str,
                        help="Creates/Appends to given CSV file instead of writing to terminal")
    parser.add_argument('--db', metavar="DBFILE", type=str,
                        help="Creates/Appends to given DB file instead of writing to terminal")
    parser.add_argument('--convert_csv_to_db', action='append', nargs=2, metavar=("CSVFILE", "DBFILE"), type=str,
                        help="Converts a CSV to a DB")
    parser.add_argument('--convert_db_to_csv', action='append', nargs=2, metavar=("DBFILE", "CSVFILE"), type=str,
                        help="Converts a DB to a CSV")
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    instances_data = {}

    if not (args.convert_csv_to_db or args.convert_db_to_csv):
        for instance in args.instances:
            print('Fetching instance data for %s' % instance)
            instance_api_v1_data = get_api_v1_data_of_instance(instance)
            instance_api_v2_data = get_api_v2_data_of_instance(instance)
            instances_data[instance] = {
                'title': instance_api_v1_data['title'],
                'user_count': instance_api_v1_data['stats']['user_count'],
                'active_users': instance_api_v2_data['usage']['users']['active_month'],
                'status_count': instance_api_v1_data['stats']['status_count'],
                'domain_count': instance_api_v1_data['stats']['domain_count']
            }

    if args.csv:
        print('Writing CSV to %s' % args.csv)
        write_csv(instances_data, args.csv)
        sys.exit(0)
    if args.db:
        print('Writing DB to %s' % args.db)
        insert_data_into_database(instances_data, args.db)
        sys.exit(0)
    if args.convert_csv_to_db:
        source_csv = args.convert_csv_to_db[0][0]
        target_db = args.convert_csv_to_db[0][1]
        print('Converting the CSV file: %s' % source_csv)
        print('to the SQLite database:  %s' % target_db)
        convert_csv_to_db(source_csv, target_db)
        sys.exit(0)
    if args.convert_db_to_csv:
        source_db = args.convert_db_to_csv[0][0]
        target_csv = args.convert_db_to_csv[0][1]
        print('Converting the DB file: %s' % source_db)
        print('to the CSV file:        %s' % target_csv)
        convert_db_to_csv(source_db, target_csv)
        sys.exit(0)

    # Printing the whole Mastodon instance stats
    if not (args.convert_csv_to_db or args.convert_db_to_csv):
        print('=============== Mastodon instance stats v2.0.0 ===============')
        for instance in args.instances:
            data = instances_data[instance]
            print_stats_of_single_instance(data['title'], data['user_count'], data['status_count'],
                                           data['domain_count'], data['active_users'])

        if len(instances_data) == 2:
            data_left = instances_data[args.instances[0]]
            data_right = instances_data[args.instances[1]]

            print('=== Comparisons ===')
            print_comparisons('Total Users', data_left['title'], data_right['title'], data_left['user_count'],
                              data_right['user_count']),
            print_comparisons('Active Users', data_left['title'], data_right['title'], data_left['active_users'],
                              data_right['active_users'])
            print_comparisons('Toots', data_left['title'], data_right['title'], data_left['status_count'],
                              data_right['status_count'])
            print_comparisons('Connections', data_left['title'], data_right['title'], data_left['domain_count'],
                              data_right['domain_count'])


if __name__ == "__main__":
    main()
