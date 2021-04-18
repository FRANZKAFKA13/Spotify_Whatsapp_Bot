import numpy as np 
import pandas as pd

def read_artists_csv():
    artists = pd.read_csv("../data/artists.csv", sep=";")
    return artists

def read_users_csv():
    users = pd.read_csv("../data/users.csv", sep=";")
    return users
