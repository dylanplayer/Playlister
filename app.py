from flask import Flask, render_template, redirect, url_for, request
from bson.objectid import ObjectId
from pymongo import MongoClient
import os

app = Flask(__name__)

# Start DB with: brew services start mongodb-community@5.0 
# Stop DB with: brew services stop mongodb-community@5.0

host = os.environ.get('MONGODB_URI','mongodb+srv://Atlas-Admin:AyaKcgVdV7eCeojW@playlister.y7ywm.mongodb.net/playlists?retryWrites=true&w=majority')
client = MongoClient(host=host)
db = client.get_default_database()
playlists = db.playlists

@app.route('/')
def index():
    return redirect('/playlists')

@app.route('/playlists', methods=['GET'])
def playlists_index():
    return render_template('playlists_index.html', playlists=playlists.find())

@app.route('/playlists', methods=['POST'])
def playlists_submit():
    video_ids = str(request.form.get('video_ids')).split()
    videos = video_url_creator(video_ids)
    playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': videos,
        'video_ids': video_ids,
    }
    playlists.insert_one(playlist)
    return redirect(url_for('playlists_index'))

@app.route('/playlists/new')
def playlists_new():
    return render_template('playlists_new.html', playlist={}, title='New Playlist')

@app.route('/playlists/<playlist_id>')
def playlists_show(playlist_id):
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    return render_template('playlists_show.html', playlist=playlist)

@app.route('/playlists/<playlist_id>', methods=['POST'])
def playlists_update(playlist_id):
    video_ids = request.form.get('video_ids').split()
    videos = video_url_creator(video_ids)
    updated_playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': videos,
        'video_ids': video_ids
    }
    playlists.update_one(
        {'_id': ObjectId(playlist_id)},
        {'$set': updated_playlist})
    return redirect(url_for('playlists_show', playlist_id=playlist_id))

@app.route('/playlists/<playlist_id>/edit')
def playlists_edit(playlist_id):
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    return render_template('playlists_edit.html', playlist=playlist, title='Edit Playlist')

@app.route('/playlists/<playlist_id>/delete', methods=['POST'])
def playlists_delete(playlist_id):
    playlists.delete_one({'_id': ObjectId(playlist_id)})
    return redirect(url_for('playlists_index'))

def video_url_creator(ids):
    videos = []
    for id in ids:
        video = 'https://youtube.com/embed/' + id
        videos.append(video)
    return videos

if __name__ == '__main__':
    app.run(debug=True)
