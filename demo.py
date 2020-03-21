#!/usr/bin/env python3

import sys
import spotipy
import spotipy.util as util
import lyricsgenius

import pprint

genius = lyricsgenius.Genius("MGsI9MWlymRLnGmJ_HKdQlxxHXwWSGKWFGElUQUdT3q08gShQIE4x-6U527PlqQY")
genius.verbose = False # Turn off status messages
genius.remove_section_headers = True # Remove section headers (e.g. [Chorus]) from lyrics when searching

words = {}

def add_words(lyrics):
    for word in lyrics:
        word = word.lower().strip().replace('"','').replace(',','').replace('.','').strip('\'').strip('‘').replace('?','').strip('(').strip(')')
        words[word] = words.get(word,0) + 1

def get_lyrics(artist, name):
    song = genius.search_song(name, artist)
    lyrics = song.lyrics
    add_words(lyrics.split())

def get_track_info(tracks):
    for item in tracks['items']:
        track = item['track']
        artist = track['artists'][0]['name']
        name = track['name']
        get_lyrics(artist, name)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
        plist = sys.argv[2]
    else:
        print("Whoops, need your username and the name of the playlist!")
        print("usage: python playlist.py [username] [playlist]")
        sys.exit()

    token = util.prompt_for_user_token(username)

    if token:
        sp = spotipy.Spotify(auth=token)
        playlists = sp.current_user_playlists()
        for playlist in playlists['items']:
            if playlist['name'] == plist:
                print()
                print(f'The most used words in your playlist {plist}: ')
                results = sp.playlist(playlist['id'], fields="tracks,next")
                tracks = results['tracks']
                get_track_info(tracks)
                while tracks['next']:
                    tracks = sp.next(tracks)
                    get_track_info(tracks)

        words = sorted(words.items(), key=lambda x: x[1], reverse=True)
        
        for word in words:
            output = word[0] + ': ' + str(word[1])
            print(output)

    else:
        print("Can't get token for", username)
