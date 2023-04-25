# Mastodon instance stats
Displaying some stats of any Mastodon instance and compare them to a other Mastodon instance.

### Requirements
- Python3
- Unix shell
- Python3 repuests
- Wget (optional)

### Installation
##### Debian/Ubuntu
- `apt install python3`
- `wget https://raw.githubusercontent.com/do-m-inik/mastodon-instance-stats/main/requirements.txt`
- `pip install  -r requirements.txt`
- `wget https://raw.githubusercontent.com/do-m-inik/mastodon-instance-stats/main/mastodon-instance-stats.py`

##### MacOS
- `brew install python3`
- `wget https://raw.githubusercontent.com/do-m-inik/mastodon-instance-stats/main/requirements.txt`
- `python3 -m pip install -r requirements.txt`
- `wget https://raw.githubusercontent.com/do-m-inik/mastodon-instance-stats/main/mastodon-instance-stats.py`

### Usage
- `python3 mastodon-instance-stats.py [-h] [--csv <CSV file name>] <instance 1> [<other instances> ...]`
- For every given instance the script returns the stats of the given Mastodon instances
- If two Mastodon instances are given the script compares the two given instances
- With `--csv <file name>` the stats are saved into an CSV instead of printing them out

### Examples
- `python3 mastodon-instance-stats.py bahn.social`
<br />
Output:

    =============== Mastodon instance stats ===============
    === Bahn.Social ===
    Users: 82
    Posts: 24994
    Connections: 9383

<br />

- `python3 mastodon-instance-stats.py bahn.social chaos.social`
<br />
Output:

    =============== Mastodon instance stats ===============
    === Bahn.Social ===
    Users: 82
    Posts: 24994
    Connections: 9383

    === chaos.social ===
    Users: 10903
    Posts: 4090830
    Connections: 52995

    === Comparisons ===
    = users =
    Difference: 10821
    Ratio Bahn.Social/chaos.social: 0.75 %
    How many Bahn.Social users per chaos.social users 132.96

    = posts =
    Difference: 4065836
    Ratio Bahn.Social/chaos.social: 0.61 %
    How many Bahn.Social toots per chaos.social posts 163.67

    = connections =
    Difference: 43612
    Ratio Bahn.Social/chaos.social: 17.71 %
    How many Bahn.Social connections per chaos.social connections 5.65

<br />

- `python3 mastodon-instance-stats.py bahn.social chaos.social bonn.social`
<br />
Output:

    =============== Mastodon instance stats ===============
    === Bahn.Social ===
    Users: 82
    Toots: 25021
    Connections: 9383
    
    === chaos.social ===
    Users: 10905
    Toots: 4093387
    Connections: 53010
    
    === Bonn.social ===
    Users: 1258
    Toots: 172075
    Connections: 23561

<br />

- `python3 mastodon-instance-stats.py --csv example.csv bahn.social chaos.social`
<br />
example.csv:

    Date and time,Instance name,Domain,Users,Toots,Connections
    2023-04-25Z19:39:46.507849,Bahn.Social,bahn.social,82,25021,9383
    2023-04-25Z19:39:46.507849,chaos.social,chaos.social,10905,4093484,53010
    
<br />
