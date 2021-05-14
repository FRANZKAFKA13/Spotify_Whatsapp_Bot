import sqlite3
from sqlalchemy import create_engine

import numpy as np 
import pandas as pd


def create_db_connection(db_file):
    """ Create a database connection to the SQLite database specified by db_file
    Args:
        db_file: database file
    Returns:
        conn: Connection object or None
    """

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)

    return conn


def create_initial_db(db_file):
    """ Set up initial DB with default tables
    Args:
        db_file: database file
    """
    conn = create_db_connection(db_file)
    cur = conn.cursor()

    sql_create_users_table =              """ CREATE TABLE "users" (
                                              "user_uri"    TEXT NOT NULL UNIQUE,
                                              "user_name"	TEXT,
                                              PRIMARY KEY("user_uri")
                                              ); """

    sql_create_subscribed_artists_table = """ CREATE TABLE "subscribed_artists" (
	                                          "user_uri"	INTEGER NOT NULL,
	                                          "artist_uri"	TEXT NOT NULL,
                                              FOREIGN KEY(user_uri) REFERENCES users(user_uri),
                                              UNIQUE(user_uri, artist_uri)
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


def add_user(db_file, user_uri, user_name):
    """ Add user URI to database user table
    Args:
        db_file: Database file
        user_name (string): The user's name
    """

    conn = create_db_connection(db_file)
    cur = conn.cursor()

    # Add new user to user table
    new_user = (user_uri, user_name)
    sql_add_new_user = """ INSERT INTO users(user_uri, user_name)
                           VALUES(?,?) """

    try:
        cur.execute(sql_add_new_user, new_user)
    except Exception as e:
        print("Failed adding entry to table users: " + str(e))
    

    conn.commit()
    cur.close()


def add_subscription(db_file, user_uri, artist_uri):
    """ Add subscription (artist_uri) to user
    Args:
        db_file: Database file
        user_uri (string): The user's URI
        artist_uri (string): The artist's URI
    """
    conn = create_db_connection(db_file)
    cur = conn.cursor()

    # Add new subscription to user table
    new_subscription = (user_uri, artist_uri)
    sql_add_new_user = """ INSERT INTO subscribed_artists(user_uri, artist_uri)
                           VALUES(?,?) """

    try:
        cur.execute(sql_add_new_user, new_subscription)
    except Exception as e:
        print("Failed adding new subscription: " + str(e))
    

    conn.commit()
    cur.close()


def get_subscribed_artists(db_file, user_uri):
    """A function returning artists user subscribed to from the database.
    Args:
        user_uri (string): The user's URI.
    Returns:
        artist_uri_list (list): A list of URIs of subscribed artists.
    """

    conn = create_db_connection(db_file)
    cur = conn.cursor()

    sql_get_user_subscriptions =    """ SELECT artist_uri 
                                    FROM subscribed_artists
                                    WHERE user_uri = ? """
    try:
        artist_uri_query_result = cur.execute(sql_get_user_subscriptions, (user_uri,)).fetchall()
    except Exception as e:
        print("test")
        print("Failed pulling user subscriptions: " + str(e))
    
    artist_uri_list = []
    for artist_uri in artist_uri_query_result:
        artist_uri_list.append(artist_uri[0])

    conn.commit()
    cur.close()

    return artist_uri_list



#create_initial_db("../../data/test.db")
#add_user("../../data/test.db", "test_uri", "Even more user")
# add_subscription("../../data/test.db", "test_uri", "artist_4")
# print(get_subscribed_artists("../../data/test.db", "test_uri"))