# Mastodon instance stats
Displaying and saving some stats of any Mastodon instance and compare them to a other Mastodon instance.

## Requirements
- Python3
- Unix shell
- Wget (optional)

## Installation
#### Debian/Ubuntu
- `apt install python3`
- `wget https://raw.githubusercontent.com/do-m-inik/mastodon-instance-stats/main/requirements.txt`
- `pip install -r requirements.txt`
- `wget https://raw.githubusercontent.com/do-m-inik/mastodon-instance-stats/main/mastodon-instance-stats.py`

#### MacOS
- `brew install python3`
- `wget https://raw.githubusercontent.com/do-m-inik/mastodon-instance-stats/main/requirements.txt`
- `python3 -m pip install -r requirements.txt`
- `wget https://raw.githubusercontent.com/do-m-inik/mastodon-instance-stats/main/mastodon-instance-stats.py`

## Usage
- `python3 mastodon-instance-stats.py [-h] [--csv CSVFILE] [--db DBFILE] [--convert_csv_to_db CSVFILE DBFILE] [INSTANCE ...]`
- For every given instance the script returns the stats of the given Mastodon instances
- If two Mastodon instances are given the script compares the two given instances
- With `--csv <file name>` the stats of the given Mastodon instances are saved into an CSV without comparison instead of printing them out
- With `--db <file name>` the stats of the given Mastodon instances are saved into an SQLite DB without comparison instead of printing them out
- With `--convert_csv_to_db <csv file name> <db file name>` a CSV gets converted into a SQLite DB
- With `--convert_db_to_csv <db file name> <csv file name>` a DB gets converted into a SQLite CSV

## Examples
- 1 given Mastodon instance: `python3 mastodon-instance-stats.py bahn.social`
<br />
Output:

    Fetching instance data for bahn.social
    =============== Mastodon instance stats v2.0.0 ===============
    === Bahn.Social ===
    Total Users:  214
    Active Users: 122
    > Ratio:      57.01 %
    Toots:        41242
    Connections:  12888

<br />

- 2 given Mastodon instances: `python3 mastodon-instance-stats.py bahn.social chaos.social`
<br />
Output:

    Fetching instance data for bahn.social
    Fetching instance data for chaos.social
    ============== Mastodon instance stats v2.0.0 ===============
    === Bahn.Social ===
    Total Users:  214
    Active Users: 122
    > Ratio:      57.01 %
    Toots:        41242
    Connections:  12888

    === chaos.social ===
    Total Users:  11175
    Active Users: 5988
    > Ratio:      53.58 %
    Toots:        4736675
    Connections:  58043

    === Comparisons ===
    = Total Users =
    Difference: 10961
    Ratio Bahn.Social/chaos.social: 1.91 %
    How many chaos.social total users per Bahn.Social total user: 52.22

    = Active Users =
    Difference: 5866
    Ratio Bahn.Social/chaos.social: 2.04 %
    How many chaos.social active users per Bahn.Social active user: 49.08

    = Toots =
    Difference: 4695433
    Ratio Bahn.Social/chaos.social: 0.87 %
    How many chaos.social toots per Bahn.Social toot: 114.85

    = Connections =
    Difference: 45155
    Ratio Bahn.Social/chaos.social: 22.2 %
    How many chaos.social connections per Bahn.Social connection: 4.5

<br />

- 3 given Mastodon instances: `python3 mastodon-instance-stats.py bahn.social chaos.social bonn.social`
<br />
Output:

    Fetching instance data for bahn.social
    Fetching instance data for chaos.social
    Fetching instance data for bonn.social
    =============== Mastodon instance stats v2.0.0 ===============
    === Bahn.Social ===
    Total Users:  214
    Active Users: 122
    > Ratio:      57.01 %
    Toots:        41242
    Connections:  12888

    === chaos.social ===
    Total Users:  11175
    Active Users: 5988
    > Ratio:      53.58 %
    Toots:        4736675
    Connections:  58043

    === Bonn.social ===
    Total Users:  1300
    Active Users: 484
    > Ratio:      37.23 %
    Toots:        194003
    Connections:  26643

<br />

- 2 given Mastodon instances gets saved into a CSV: `python3 mastodon-instance-stats.py --csv example.csv bahn.social chaos.social`
<br />
example.csv:

    Date and time,Instance name,Domain,Users,Active users,Toots,Connections,DUsers,DActive users,DToots,DConnections
    2023-08-15 11:57:39.575236,Bahn.Social,bahn.social,214,122,41242,12888,214,122,41242,12888
    2023-08-15 11:57:39.575236,chaos.social,chaos.social,11175,5988,4736675,58043,11175,5988,4736675,58043
    
<br />

- A given Mastodon instance gets saved into a DB: `python3 mastodon-instance-stats.py --db example.db bahn.social`
<br />
<br />

- A given CSV gets converted into a DB: `python3 mastodon-instance-stats.py --convert_csv_to_db example.csv example.db`
<br />
<br />

- A given DB gets converted into a CSV: `python3 mastodon-instance-stats.py --convert_db_to_csv example.db example.csv`
