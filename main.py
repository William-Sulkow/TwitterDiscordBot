import asyncio
from datetime import time
from pprint import pprint

import spotipy
import discord
from discord.ext import commands

# SPOTIFY
username = ""
client_id = ""
client_secret = ""
redirect_url = "https://google.com/"

oauth = spotipy.SpotifyOAuth(client_id, client_secret, redirect_url,
                             scope='streaming user-modify-playback-state app-remote-control streaming user-read-playback-state')

token_dict = oauth.get_access_token()
token = token_dict['access_token']

spotify = spotipy.Spotify(oauth_manager=oauth)


def get_song(search_query):
    searchResults = spotify.search(search_query, 1, 0, "track")
    tracks_dict = searchResults['tracks']
    tracks_items = tracks_dict['items']
    return tracks_items[0]


def play_song(item):
    spotify.start_playback(device_id=spotify.devices()["devices"][0]["id"], uris=item)


def add_to_queue(item):
    spotify.add_to_queue(uri=item[0])


def get_playing_song():
    return spotify.currently_playing()["item"]


def next_song():
    spotify.next_track()


# DISCORD
bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command()
async def play(ctx, *name):
    await asyncio.sleep(0.3)
    song = get_song(" ".join(name))
    if spotify.currently_playing()['progress_ms'] == 0:
        play_song([song["uri"]])
        title = f"Playing: {song['name']}"
    else:
        add_to_queue([song["uri"]])
        title = f"Queueing: {song['name']}"

    description = f"**By: {', '.join([artist['name'] for artist in song['artists']])}**"
    embed = discord.Embed(title=title, description=description, color=discord.Color.gold())

    embed.set_thumbnail(url=song["album"]["images"][0]["url"])
    await ctx.send(embed=embed)


@bot.command()
async def play_album(ctx, *name):
    searchResults = spotify.search(" ".join(name), 1, 0, "album")
    tracks_dict = searchResults['album']
    tracks_items = tracks_dict['items']
    pprint(tracks_items[0])


@bot.command()
async def next(ctx):
    song = get_playing_song()
    title = f"Skipping: {song['name']}"

    description = f"**By: {', '.join([artist['name'] for artist in song['artists']])}**"
    embed = discord.Embed(title=title, description=description, color=discord.Color.gold())

    embed.set_thumbnail(url=song["album"]["images"][0]["url"])
    await ctx.send(embed=embed)

    next_song()


bot.run('')
