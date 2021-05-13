import numpy as np 
import pandas as pd

def read_artists_csv():
    path = "../data/artists.csv"
    artists = pd.read_csv(path, sep=";")
    print("Log: Data read from path: " + path)
    return artists

def read_users_csv():
    path = "../data/users.csv"
    users = pd.read_csv(path, sep=";")
    print("Log: Data read from path: " + path)
    return users
