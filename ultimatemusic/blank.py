#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 10:22:25 2021

@author: rainmaker
"""

import youtube_dl
import ffmpeg
from dotenv import load_dotenv
import os

load_dotenv()
API = os.getenv('YOUTUBE_API')

#youtube#video
#youtube#playlist

api_name = "youtube"
api_version = "v3"

from googleapiclient.discovery import build
youtube = build(api_name,api_version,developerKey = API)


request = youtube.search().list(
    part = 'snippet',
    maxResults = 10,
    q = "Nonagon Infinity"    
    )

responses = request.execute()

top_result = responses['items'][0]

res_id = top_result['id']


class Queue:
    def __init__(self,argument):
        self.keyword = argument
        self.URL = {}
        self.songs = []
    
    def get_url(self, keyword = None):
        if keyword is None:
            query = self.keyword
        else:
            query = keyword
        request = youtube.search().list(
            part = 'snippet',
            maxResults = 10,
            q = query
            )
        responses = request.execute()
        top_result = responses['items'][0]['id']
        if top_result['kind'] == "youtube#video":
            url_type = "video"
            url = "https://www.youtube.com/watch?v="+top_result['videoId']
        if top_result['kind'] == "youtube#playlist":
            url_type = "playlist"
            url = top_result['playlistId']
        if top_result['kind'] == "youtube#channel":
            url_type = "channel"
            url = top_result['channelId']
        URL = {'link' : url,
           'type' : url_type
           }
        self.URL = URL
    
    def get_video(self):
        link = self.URL['link']
        self.songs.append(link)

    def get_playlist(self):
        request = youtube.playlistItems().list(
            part = "snippet, contentDetails",
            maxResults = 10,
            playlistID = self.URL['link']
            )
        response = request.execute()
        playlist_items = response['items']
        for video in playlist_items:
            video_id = video['contentDetails']['videoId']
            self.songs.append("https://www.youtube.com/watch?v="+video_id)
    
    def get_playlist_from_channel(self):
        """request = youtube.channelSections().list(
            part = "snippet, contentDetails",
            channelID = self.URL['link']
            )
        response = request.execute()
        playlistId = response['items']"""
        pass
    
    
    
    
    def route(self):
        if self.URL['type'] == "video":
            self.get_video()
        if self.URL['type'] == "playlist":
            self.get_playlist()
        if self.URL['type'] == "channel":
            pass       
    def enqueue(self):
        self.get_url()
        self.route()
        
    def remove_from_queue(song):
        if song in self.songs:
            self.songs.remove(song)
  
        
  
   
request = youtube.channelSections().list(
    part = "snippet, contentDetails",
    channelId =  "UCNiyS8zr2RIddszLwtoyUow"   
    )
response = request.execute()

    
"""



    