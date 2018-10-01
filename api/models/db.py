import psycopg2
from psycopg2.extras import RealDictCursor


class DB():
    def __init__(self, host, user, dbname, password):
        try:
            self.connection = psycopg2.connect(

                host="localhost",
                user="postgres",
                dbname="fastfoodsapi",
                password="sudo"
            )
            print('connection succeful {}'.format(dbname))
        except(Exception, psycopg2.DatabaseError) as e:
            print(e)


db = DB(host="localhost",
        user="postgres",
        dbname="fastfoodsapi",
        password="sudo")
