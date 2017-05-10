"""

This module provides a class for handling the database stuff in the operator
instructions module.
"""

import psycopg2
import logging

class DatabaseHandler():
    """

    Handles connecting to the database and provides methods for retrieving
    raspberry pi config info, running recipes, and filenames for the running
    recipe.
    """

    def __init__(
            self,
            host='10.51.50.21',
            database='plantfloor',
            user='ryan',
            password=None):
        """

        Initialize the database connection parameters
        """
        self.user = user
        self.password = password
        self.host = host
        self.database = database

    def get_current_running_recipe(self, machine_id):
        """

        Connect to the database and get the running partnumber.
        """
        try:
            db_connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user)
            cursor = db_connection.cursor()
            query = ("select running_recipe_id from "
                     "productiondata_livedata where machine_id=%s;")
            cursor.execute(query, (machine_id,))
            recipe = cursor.fetchall()
            db_connection.close()
            if bool(recipe):
                return recipe[0][0]
            else:
                return None
        except psycopg2.Error as error:
            logging.error(error)

    def get_current_recipe_filename(self, unit_id, recipe):
        """

        Connect to the database and retrieve the document number.
        """
        try:
            db_connection = psycopg2.connect(
                host=self.host,
                database=self.database)
            cursor = db_connection.cursor()
            cursor.execute(
                "select doc_url from rpimanager_rpiconfig where rpi_id=%s "
                "and partnumber_id=%s;", (unit_id, recipe,))
            filenames_list = cursor.fetchall()
            db_connection.close()
            if bool(filenames_list):
                return filenames_list[0][0]
            else:
                return None
        except psycopg2.Error as error:
            logging.error(error)

    def get_rpi_config(self, hostname):
        """

        Connect to the database and get the raspberry pi config
        info.
        """
        try:
            db_connection = psycopg2.connect(
                host=self.host,
                database=self.database)
            cursor = db_connection.cursor()
            cursor.execute(
                "select * from rpimanager_rpiunit where hostname=%s;",
                (hostname,))
            config = cursor.fetchall()
            db_connection.close()
            if bool(config):
                return config[0]
            else:
                return None
        except psycopg2.Error as error:
            logging.error(error)

    def get_rpi_version(self):
        """

        Connect to the database and get the raspberry pi config
        info.
        """
        try:
            db_connection = psycopg2.connect(
                host=self.host,
                database=self.database)
            cursor = db_connection.cursor()
            cursor.execute(
                "select * from rpimanager_rpiversion order by id desc "
                "limit 1;")
            config = cursor.fetchall()
            db_connection.close()
            if bool(config):
                return config[0]
            else:
                return None
        except psycopg2.Error as error:
            logging.error(error)

    def get_all_files(self, unit_id, recipe):
        """

        Connect to the database and get all the files configured for
        this recipe.
        """
        try:
            db_connection = psycopg2.connect(
                host=self.host,
                database=self.database)
            cursor = db_connection.cursor()
            cursor.execute(
                "select doc_url from rpimanager_rpiconfig where rpi_id=%s "
                "and partnumber_id=%s;", (unit_id, recipe,))
            filenames_list = cursor.fetchall()
            db_connection.close()
            if bool(filenames_list):
                return [x[0] for x in filenames_list]
            else:
                return None
        except psycopg2.Error as error:
            logging.error(error)
