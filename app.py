from flask import Flask, render_template

app = Flask(__name__)

playlists = [
    { 
        'title': 'Cat Videos',
        'description': 'Cats acting weird.'
    },
    { 
        'title': '80/s Music',
        'description': 'Don\'t stop believing!'
    },
]

@app.route('/')
def index():
    return render_template('index.html', msg='Flask is cool!!')

@app.route('/playlists')
def playlists_index():
    return render_template('playlists_index.html', playlists=playlists)

if __name__ == '__main__':
    app.run(debug=True)