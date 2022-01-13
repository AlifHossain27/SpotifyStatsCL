import os
import json
import requests
from datetime import date
from refresh import Refresh
from simple_term_menu import TerminalMenu

user_id = os.getenv("USER_ID")

class SpotifyStats:
    def __init__(self):
        self.user = user_id
        self.token = ""
        self.user_top_tracks=None
        self.user_top_artists=None
        self.user_top_genres=None
        

    # User Top Tracks
    def top_track(self):
        top_tracks = []
        top_tracks_id = []
        query = "https://api.spotify.com/v1/me/top/tracks"

        response = requests.get(query,
                                headers={"Content-Type": "application/json",
                                         "Authorization": "Bearer {}".format(self.token)})
        
        response_json= response.json()

        for i in response_json["items"]:
            top_tracks.append(i["album"]["name"])
            top_tracks_id.append(i["album"]["id"])
        
        self.user_top_tracks=top_tracks_id[:5]
        
        return top_tracks[:5]
        
        

    # User Top Artists
    def top_artist(self):
        top_artist = []
        top_artist_id = []

        query = "https://api.spotify.com/v1/me/top/artists"

        response = requests.get(query,
                                headers={"Content-Type": "application/json",
                                         "Authorization": "Bearer {}".format(self.token)})
        
        response_json= response.json()
        
        for i in response_json["items"]:
            top_artist.append(i["name"])
            top_artist_id.append(i["id"])
        
        
        self.user_top_artists=top_artist_id[:5]

        return top_artist[:5]

    # User Top Genres
    def top_genres(self):
        top_genres=[]
        query = "https://api.spotify.com/v1/me/top/artists"

        response = requests.get(query,
                                headers={"Content-Type": "application/json",
                                         "Authorization": "Bearer {}".format(self.token)})
        
        response_json= response.json()
        
        for i in response_json["items"]:
            for g in i["genres"]:
                top_genres.append(g)
        
        top_genres=list(set(top_genres))
        self.user_top_genres = top_genres[:5]
        
        return top_genres[:5]

    def call_refresh(self):
        print("Refreshing token...")

        refreshCaller = Refresh()
        self.token = refreshCaller.refreshing()


if __name__=="__main__":
    stats=SpotifyStats()
    stats.call_refresh()
    # Adding Options
    options = ["Top Tracks","Top Artists","Top Genres","Quit"]

    mainMenu = TerminalMenu(options,title="Spotify Stats")

    quitting = False
    while quitting == False:
        optionsIndex=mainMenu.show()
        optionsChoice=options[optionsIndex]

        if optionsChoice == 'Quit':
            quitting = True

        if optionsChoice == "Top Tracks":
            print("Top Tracks")
            print("-----------")
            for tracks in stats.top_track():
                print(tracks)
        
        if optionsChoice == "Top Artists":
            print("Top Artists")
            print("------------")
            for artists in stats.top_artist():
                print(artists)
        
        if optionsChoice == "Top Genres":
            print("Top Genres")
            print("-----------")
            for genres in stats.top_genres():
                print(genres)