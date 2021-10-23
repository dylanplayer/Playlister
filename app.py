from flask import Flask, render_template, redirect
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

@app.route('/playlists')
def playlists_index():
    return render_template('playlists_index.html', playlists=playlists.find())

if __name__ == '__main__':
    app.run(debug=True)