import sqlite3
import sqlalchemy
from sqlalchemy import create_engine

import numpy as np 
import pandas as pd


def get_subscribed_artist(user_name):
    """A function returning artists user subscribed to from the database.

    Args:
        user_name (String): The user's name.

    Returns:
        artist_uri_list: A list of URIs of subscribed artists.
    """

    engine = create_engine('sqlite:///test.db')
    df = pd.read_sql_table('subscribed_artists', engine)

    print(df)

    return ""


def create_connection(db_file):
    """ Create a database connection to the SQLite database specified by db_file

    Args:
        db_file: database file
    
    Returns:
        conn: Connection object or None
    """

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def create_initial_db(db_file):

    conn = create_connection(db_file)
    cur = conn.cursor()

    sql_create_users_table =              """ CREATE TABLE "users" (
                                              "user_id"	INTEGER NOT NULL UNIQUE,
                                              "name"	INTEGER,
                                              PRIMARY KEY("user_id")
                                              ); """

    sql_create_subscribed_artists_table = """ CREATE TABLE "subscribed_artists" (
	                                          "user_id"	INTEGER NOT NULL,
	                                          "artist_uri"	TEXT NOT NULL,
                                              FOREIGN KEY(user_id) REFERENCES users(user_id)
                                              ); """

    try:
        cur.execute(sql_create_users_table)
    except Exception as e:
        print("Failed creating new table: " + str(e))

    try:
        cur.execute(sql_create_subscribed_artists_table)
    except Exception as e:
        print("Failed creating new table: " + str(e))

    conn.commit()
    cur.close()


def add_user(db_file, user_name):

    conn = create_connection(db_file)
    cur = conn.cursor()

    # Generate new user ID by iterating
    sql_get_latest_user_id = """ SELECT max(user_id) FROM users"""
    cur.execute(sql_get_latest_user_id)
    latest_id = cur.fetchall()[0][0]
    if latest_id is None:
        new_id = 1
    else:
        new_id = latest_id + 1

    # Add new user to user table
    new_user = (new_id, user_name)
    sql_add_new_user = """ INSERT INTO users(user_id, name)
                           VALUES(?,?) """

    try:
        cur.execute(sql_add_new_user, new_user)
    except Exception as e:
        print("Failed adding entry to table users: " + str(e))
    

    conn.commit()
    cur.close()


def add_subscription(db_file, user_id, artist_uri):

    conn = create_connection(db_file)
    cur = conn.cursor()

    # Add new subscription to user table
    new_subscription = (user_id, artist_uri)
    sql_add_new_user = """ INSERT INTO subscribed_artists(user_id, artist_uri)
                           VALUES(?,?) """

    try:
        cur.execute(sql_add_new_user, new_user)
    except Exception as e:
        print("Failed adding entry to table users: " + str(e))
    

    conn.commit()
    cur.close()


create_initial_db("../../data/test.db")
add_user("../../data/test.db", "Even more user")