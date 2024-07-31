import sqlite3

def dump_sqlite_to_sqlite_file(sqlite_file, output_file):
    conn = sqlite3.connect(sqlite_file)
    with open(output_file, 'w') as f:
        for line in conn.iterdump():
            f.write('%s\n' % line)
    conn.close()

dump_sqlite_to_sqlite_file('site.db', 'dump.sql')

