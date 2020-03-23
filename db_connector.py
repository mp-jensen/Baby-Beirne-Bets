import MySQLdb as mariadb
import os

# get environment variables from heroku to connect to the database
db_url = os.environ['CLEARDB_DATABASE_URL']

db_url = db_url.replace('/',' ').replace(':',' ').replace('@',' ').replace('?',' ').split()
user = db_url[1]
passwd = db_url[2]
host = db_url[3]
db = db_url[4]

def connect_to_database(host = host, user = user, passwd = passwd, db = db):
    '''
    connects to a database and returns a database objects
    '''
    print("user: {0}, passwd: {1}, host: {2}, db: {3}".format(user, passwd, host, db))
    db_connection = mariadb.connect(host,user,passwd,db)
    return db_connection

def execute_query(db_connection = None, query = None, query_params = ()):
    '''
    executes a given SQL query on the given db connection and returns a Cursor object

    db_connection: a MySQLdb connection object created by connect_to_database()
    query: string containing SQL query

    returns: A Cursor object as specified at https://www.python.org/dev/peps/pep-0249/#cursor-objects.
    You need to run .fetchall() or .fetchone() on that object to actually acccess the results.

    '''

    if db_connection is None:
        print("No connection to the database found! Have you called connect_to_database() first?")
        return None

    if query is None or len(query.strip()) == 0:
        print("query is empty! Please pass a SQL query in query")
        return None

    print("Executing %s with %s" % (query, query_params));
    # Create a cursor to execute query. Why? Because apparently they optimize execution by retaining a reference according to PEP0249
    cursor = db_connection.cursor()

    cursor.execute(query, query_params)
    # this will actually commit any changes to the database. without this no
    # changes will be committed!
    db_connection.commit();
    return cursor

