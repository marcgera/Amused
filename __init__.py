from flask import Flask,render_template, request
from classes.AmusedDB import AmusedDB
import json
import platform
import os

db = AmusedDB()
db.create_db()
db.populateDB()

global user_ID
global playlist_ID

app = Flask(__name__)

@app.route('/')
def index():
    return 'Amused app. Use e.g. http://127.0.0.1:81/therapist?user_ID=1 for therapist screen'

@app.route('/getCategories')
def getCategories():
    return json.dumps(db.getCategories('EN'))

@app.route('/getLevels')
def getLevels():
    return json.dumps(db.getLevels('EN'))

@app.route('/getBackgrounds')
def getBackgrounds():
    return json.dumps(db.getBackgrounds('EN'))

@app.route('/getVideos', methods=['GET'])
def getVideos():
    categories_SO = int(request.args.get('categories_SO'))
    levels_SO = int(request.args.get('levels_SO'))
    backgrounds_SO = int(request.args.get('backgrounds_SO'))
    return json.dumps(db.getVideos(categories_SO, levels_SO, backgrounds_SO))

@app.route('/getMusic', methods=['GET'])
def getMusic():
    categories_SO = request.args.get('categories_SO')
    return json.dumps(db.getMusic(categories_SO))

@app.route('/therapist', methods=['GET'])
def therapist():
    global user_ID
    user_ID= request.args.get('user_ID')
    return render_template('therapist.html')

@app.route('/playlist', methods=['GET'])
def playlist():
    global playlist_ID
    playlist_ID= request.args.get('playlist_ID')
    return render_template('player.html')

@app.route('/getPlaylists')
def getPlaylists():
    return json.dumps(db.getPlaylists(user_ID))

@app.route('/removeFromPlayList', methods=['GET'])
def removeFromPlayList():
    playlistItem_ID= request.args.get('playlistitem_ID')
    return db.removeFromPlayList(playlistItem_ID)

@app.route('/editPlayListName', methods=['GET'])
def editPlayListName():
    playlist_ID= request.args.get('playlist_ID')
    playlistName = request.args.get('playlist_name')
    return db.editPlayListName(playlist_ID, playlistName)

@app.route('/getPlaylistItems', methods=['GET'])
def getPlaylistItems():
    playlist_ID = request.args.get('playlist_ID')
    return json.dumps(db.getPlaylistItems(playlist_ID))

@app.route('/getPlaylistItemsMusic', methods=['GET'])
def getPlaylistItemsMusic():
    playlist_ID = request.args.get('playlist_ID')
    return json.dumps(db.getPlaylistItemsMusic(playlist_ID))

@app.route('/getPlaylistItemsVideo', methods=['GET'])
def getPlaylistItemsVideo():
    playlist_ID = request.args.get('playlist_ID')
    return json.dumps(db.getPlaylistItemsVideo(playlist_ID))

@app.route('/getPlaylistItems2')
def getPlaylistItems2():
    global playlist_ID
    return json.dumps(db.getPlaylistItems(playlist_ID))

@app.route('/movePlayListItem', methods=['GET'])
def movePlayListItem():
    playlistItem_ID= request.args.get('playlistitem_ID')
    direction = request.args.get('direction')
    tableName = request.args.get('tableName')
    db.movePlaylistitem(playlistItem_ID, tableName, direction)
    return 'http200OK'

@app.route('/add2PlaylistItems', methods=['GET'])
def add2PlaylistItems():
    playlist_ID = request.args.get('playlist_ID')
    video_ID = request.args.get('video_ID')
    music_ID = request.args.get('music_ID')
    db.add2PlaylistItems(playlist_ID, video_ID, music_ID)
    return 'http200OK'

@app.route('/addMusic2PlaylistItems', methods=['GET'])
def addMusic2PlaylistItems():
    playlist_ID = request.args.get('playlist_ID')
    music_ID = request.args.get('music_ID')
    db.addMusic2PlaylistItems(playlist_ID, music_ID)
    return 'http200OK'

@app.route('/addVideo2PlaylistItems', methods=['GET'])
def addVideo2PlaylistItems():
    playlist_ID = request.args.get('playlist_ID')
    video_ID = request.args.get('video_ID')
    db.addVideo2PlaylistItems(playlist_ID, video_ID)
    return 'http200OK'

@app.route('/removeFromPlaylist', methods=['GET'])
def removeFromPlaylist():
    playlist_item_ID = request.args.get('playlist_item_ID')
    table_name = request.args.get('table_name')
    db.removeFromPlayList(playlist_item_ID, table_name)
    return 'http200OK'


@app.route('/addPlaylist', methods=['GET'])
def addPlaylist():
    playlist_name = request.args.get('playlist_name')
    db.addPlayList(user_ID, playlist_name)
    return 'http200OK'

@app.route('/removePlaylist', methods = ['GET'])
def removelaylist():
    playlist_ID = request.args.get('playlist_ID')
    db.removePlayList(playlist_ID)
    return 'http200OK'

app.run(host='0.0.0.0', port=81)