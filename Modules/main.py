import psycopg
#import psycopg_binary


def getConn():
    conn = psycopg.connect(
        host="localhost",
        dbname="POS",
        user="postgres",
        password="IYANN2276",
        port=5432
    )
    return conn