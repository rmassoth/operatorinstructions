"""

This module provides a class for handling the database stuff in the operator
instructions module.
"""

import psycopg2

class DatabaseHandler():
    """

    Handles connecting to the database and provides methods for retrieving
    raspberry pi config info, running recipes, and filenames for the running
    recipe.
    """

    def __init__(
            self, host='localhost', database=None, user=None, password=None):
        """Initialize the database connection parameters"""
        self.user = user
        self.password = password
        self.host = host
        self.database = database

    def get_current_running_recipe(self, machine_id):
        """Connect to the database and get the running partnumber."""
        try:
            db_connection = psycopg2.connect(
                host=self.host,
                database=self.database)
            cursor = db_connection.cursor()
            query = ("select running_recipe_id from "
                     "productiondata_livedata where machine_id=%s;")
            cursor.execute(query, (machine_id,))
            db_connection.close()
            return cursor.fetchall()[0][0]
        except psycopg2.Error as error:
            if db_connection:
                db_connection.close()
            print(error)

    def get_current_recipe_filename(self, unit_id, recipe):
        """Connect to the database and retreive the document number."""
        try:
            db_connection = psycopg2.connect(
                host=self.host,
                database=self.database)
            cursor = db_connection.cursor()
            cursor.execute(
                "select docid from rpimanager_rpiconfig where rpi_id=%s "
                "and partnumber_id;"
                , (unit_id, recipe,))
            docid = cursor.fetchall()[0][0]
            db_connection.close()
            return docid
        except psycopg2.Error as error:
            if db_connection:
                db_connection.close()
            print(error)

    def get_rpi_config(self, hostname):
        """Connect to the database and get the raspberry pi config info."""
        try:
            db_connection = psycopg2.connect(
                host=self.host,
                database=self.database)
            cursor = db_connection.cursor()
            cursor.execute(
                "select * from rpimanager_rpiunit where hostname=%s;",
                (hostname,))
            config = cursor.fetchall()[0]
            db_connection.close()
            return config
        except psycopg2.Error as error:
            if db_connection:
                db_connection.close()
            print(error)

    def get_rpi_version(self):
        """Connect to the database and get the raspberry pi config info."""
        try:
            db_connection = psycopg2.connect(
                host=self.host,
                database=self.database)
            cursor = db_connection.cursor()
            cursor.execute(
                "select * from rpimanager_rpiversion order by id desc limit 1;")
            config = cursor.fetchall()[0][0]
            db_connection.close()
            return config
        except psycopg2.Error as error:
            if db_connection:
                db_connection.close()
            print(error)
