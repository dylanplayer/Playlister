from flask import Flask, render_template, redirect, url_for, request
from bson.objectid import ObjectId
from pymongo import MongoClient

app = Flask(__name__)

# Start DB with: brew services start mongodb-community@5.0 
# Stop DB with: brew services stop mongodb-community@5.0

client = MongoClient()
db = client.Playlister
playlists = db.playlists

# playlists = [
#     { 
#         'title': 'Cat Videos',
#         'description': 'Cats acting weird.'
#     },
#     { 
#         'title': '80/s Music',
#         'description': 'Don\'t stop believing!'
#     },
# ]

@app.route('/')
def index():
    return redirect('/playlists')

@app.route('/playlists', methods=['GET'])
def playlists_index():
    return render_template('playlists_index.html', playlists=playlists.find())

@app.route('/playlists', methods=['POST'])
def playlists_submit():
    video_ids = request.form.get('video_ids').split()
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
    return render_template('playlists_new.html')

@app.route('/playlists/<playlist_id>')
def playlists_show(playlist_id):
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    return render_template('playlists_show.html', playlist=playlist)

def video_url_creator(ids):
    videos = []
    for id in ids:
        video = 'https://youtube.com/embed/' + id
        videos.append(video)
    return videos

if __name__ == '__main__':
    app.run(debug=True)