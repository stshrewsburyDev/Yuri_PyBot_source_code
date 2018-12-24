"""
YouTube API For POTATO BOT.
Made By stshrewsburyDev (AKA: Steven Shrewsbury)
"""

import argparse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def search(DEV_KEY, options):
    youtube = build("youtube", "v3", developerKey=DEV_KEY)

    search_response = youtube.search().list(q=options.q,
                                            part="id,snippet",
                                            maxResults=options.max_results
                                            ).execute()

    results = {}

    videos = []
    channels = []
    playlists = []

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append(search_result)
        elif search_result["id"]["kind"] == "youtube#channel":
            channels.append(search_result)
        elif search_result["id"]["kind"] == "youtube#playlist":
            playlists.append(search_result)

    results["videos"] = videos
    results["channels"] = channels
    results["playlists"] = playlists

    return results

def get_videos(DEV_KEY, search_query, max_results):
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", help="Serch term", default=search_query)
    parser.add_argument("--max-results", help="Max results", default=max_results)
    options = parser.parse_args()

    return search(DEV_KEY=DEV_KEY,
                  options=options)["videos"]
