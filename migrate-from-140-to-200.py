import sqlite3

def migrate_db():
    """Migrates the database structure vom v1.4.0 to v2.0.0"""

    # Establish connection to old database
    conn = sqlite3.connect('your_old_database.db') # Insert your old database name here
    cursor = conn.cursor()

    # Creating temporary database
    cursor.execute('''
        CREATE TABLE temp_table AS
        SELECT 
            date_and_time,
            instance_name,
            domain,
            users,
            0 AS active_users,
            toots,
            connections,
            d_users,
            0 AS d_active_users,
            d_toots,
            d_connections
        FROM data;
    ''')

    # Deleting the old database
    cursor.execute('DROP TABLE data;')

    # Renaming the temp database and adding primary key
    cursor.execute('''
        CREATE TABLE data (
            date_and_time DATETIME PRIMARY KEY,
            instance_name TEXT,
            domain TEXT,
            users INTEGER,
            active_users INTEGER,
            toots INTEGER,
            connections INTEGER,
            d_users INTEGER,
            d_active_users INTEGER,
            d_toots INTEGER,
            d_connections INTEGER
        );
    ''')
    cursor.execute('INSERT INTO data SELECT * FROM temp_table;')
    cursor.execute('DROP TABLE temp_table;')

    # Commit changes and closing the connection to the databse
    conn.commit()
    conn.close()

# Executing the migration
migrate_db()

