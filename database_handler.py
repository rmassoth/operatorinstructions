import psycopg2

class DatabaseHandler():

    def __init__(self, host='localhost', database=None, user=None, password=None):
        self.user = user
        self.password = password
        self.host = host
        self.database = database


    """Connect to the database and get the running partnumber."""
    def get_current_running_recipe(self, machine_id):
        try:
            db_connection = psycopg2.connect(host=self.host, database=self.database)
            cursor = db_connection.cursor()
            cursor.execute("select running_recipe_id from productiondata_livedata where machine_id=%s;", (machine_id,))
            db_connection.close()
            return cursor.fetchall()[0][0]
        except Exception as e:
            if db_connection:
                db_connection.close()
            print(e)

    """Connect to the database and retreive the document number."""
    def get_current_recipe_filename(self, unit_id, recipe):
        try:
            db_connection = psycopg2.connect(host=self.host, database=self.database)
            cursor = db_connection.cursor()
            cursor.execute("select docid from rpimanager_rpiconfig where rpi_id=%s and partnumber_id;", (unit_id, recipe,))
            docid = cursor.fetchall()[0][0]
            db_connection.close()
            return docid
        except Exception as e:
            if db_connection:
                db_connection.close()
            print(e)

    """Connect to the database and get the raspberry pi config info."""
    def get_rpi_config(self, hostname):
        try:
            db_connection = psycopg2.connect(host=self.host, database=self.database)
            cursor = db_connection.cursor()
            cursor.execute("select * from rpimanager_rpiunit where hostname=%s;", (hostname,))
            config = cursor.fetchall()[0]
            db_connection.close()
            return config
        except Exception as e:
            if db_connection:
                db_connection.close()
            print(e)

    """Connect to the database and get the raspberry pi config info."""
    def get_rpi_version(self):
        try:
            db_connection = psycopg2.connect(host=self.host, database=self.database)
            cursor = db_connection.cursor()
            cursor.execute("select * from rpimanager_rpiversion order by id desc limit 1;")
            config = cursor.fetchall()[0][0]
            db_connection.close()
            return config
        except Exception as e:
            if db_connection:
                db_connection.close()
            print(e)