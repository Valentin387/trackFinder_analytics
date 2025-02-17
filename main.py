from typing import List
from data.Song import Song
from pymongo import MongoClient, server_api
from collections import Counter
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus
from data.Song import Song
import matplotlib.pyplot as plt
import pickle

# Load environment variables
load_dotenv()

# Fetch MongoDB credentials from environment variables
MONGO_USER = os.getenv("MONGO_DB_USER")
MONGO_PASSWORD = os.getenv("MONGO_DB_PASSWORD")
if not MONGO_USER:
    raise ValueError("No user set for MongoDB. Please set the MONGO_DB_USER environment variable.")
if not MONGO_PASSWORD:
    raise ValueError("No password set for MongoDB. Please set the MONGO_DB_PASSWORD environment variable.")

# Construct MongoDB connection string
CONNECTION_STRING = (
    f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@cluster0.rskew5e.mongodb.net/"
    "?retryWrites=true&w=majority&appName=Cluster0"
)

# Connect to MongoDB
def connect_to_mongo():
    return MongoClient(CONNECTION_STRING, server_api=server_api.ServerApi("1"))

client = connect_to_mongo()
db = client.valentin_music_db

# MongoDB collections
COLLECTIONS = ["montreal_expedition", "music_2023_2", "music_2024_1", "music_2024_2", "workout_02", "workout_03"]
PICKLE_FILE = "local_exports/songs_data.pkl"

# Functions for data handling
def save_to_pickle(data, filename):
    with open(filename, "wb") as f:
        pickle.dump(data, f)

def load_from_pickle(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)

def fetch_songs_from_db() -> List[Song]:
    print("\t\t Connecting to the database, please wait ... \n")
    song_data_list = []
    for collection_name in COLLECTIONS:
        print(f"Fetching songs from {collection_name} ...")
        collection = db[collection_name]
        results = collection.find()
        song_data_list.extend(Song(**doc) for doc in results)
    print(f"Total songs retrieved: {len(song_data_list)}")
    save_to_pickle(song_data_list, PICKLE_FILE)
    return song_data_list

def plot_songs_by_genre(songs: List[Song]):
    genre_counts = Counter(song.genre for song in songs)
    plt.figure(figsize=(12, 6))
    plt.bar(genre_counts.keys(), genre_counts.values(), color="skyblue")
    plt.xlabel("Genre")
    plt.ylabel("Number of Songs")
    plt.title("Songs by Genre")
    plt.xticks(rotation=45, ha="right")
    plt.show()

def plot_songs_by_decade(songs: List[Song]):
    decade_counts = Counter()
    for song in songs:
        try:
            decade = (int(song.year) // 10) * 10
            decade_counts[decade] += 1
        except ValueError:
            continue
    plt.figure(figsize=(10, 5))
    plt.bar(decade_counts.keys(), decade_counts.values(), color="lightcoral")
    plt.xlabel("Decade")
    plt.ylabel("Number of Songs")
    plt.title("Songs by Decade")
    plt.xticks(list(decade_counts.keys()), [f"{d}s" for d in decade_counts.keys()])
    plt.show()

def main():
    print("\t\t WELCOME TO SONG DATA ANALYSIS \n")
    song_data_list = load_from_pickle(PICKLE_FILE) if os.path.exists(PICKLE_FILE) else fetch_songs_from_db()
    print(f"Total songs available: {len(song_data_list)}\n")
    while True:
        print("\nSelect an option:")
        print("1. Group songs by genre and plot the count")
        print("2. Group songs by decade and plot the count")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            plot_songs_by_genre(song_data_list)
        elif choice == "2":
            plot_songs_by_decade(song_data_list)
        elif choice == "3":
            print("Exiting program...")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()
