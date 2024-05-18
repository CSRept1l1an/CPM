import sqlite3

database = 'management.db'


def critical_log(data):

    conn = sqlite3.connect(data)
    c = conn.cursor()

    c.execute("SELECT * FROM IT_Node_KPIs WHERE Category ='critical'")

    critical_nodes = c.fetchall()

    for node in critical_nodes:
        print(node)

    c.close()
    conn.close()


critical_log(database)
