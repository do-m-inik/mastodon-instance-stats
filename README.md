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
- `pip install requests`
- `wget https://raw.githubusercontent.com/do-m-inik/mastodon-instance-stats/main/mastodon-instance-stats.py`

##### MacOS
- `brew install python3`
- `python3 -m pip install requests`
- `wget https://raw.githubusercontent.com/do-m-inik/mastodon-instance-stats/main/mastodon-instance-stats.py`

### Usage
- `python3 mastodon-instance-stats.py <choosen instance> [<compare instance>]`

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
    How many Bahn.Social usersper chaos.social users 132.96

    = posts =
    Difference: 4065836
    Ratio Bahn.Social/chaos.social: 0.61 %
    How many Bahn.Social posts per chaos.social posts 163.67

    = connections =
    Difference: 43612
    Ratio Bahn.Social/chaos.social: 17.71 %
    How many Bahn.Social connectionsper chaos.social connections 5.65