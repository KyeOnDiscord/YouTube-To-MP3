from flask import Flask, request,jsonify
from pytubefix import YouTube, Playlist

app = Flask(__name__)

@app.route("/video",methods=['GET'])
def getVideo():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "Missing 'url' query parameter"}), 400

    try:
        yt = YouTube(video_url)
        data = {
            "title": yt.title,
            "description": yt.description,
            "length_seconds": yt.length,
            "views": yt.views,
            "author": yt.author,
            "rating": yt.rating,
            "thumbnail_url": yt.thumbnail_url
        }
        print(yt)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000,debug=True)
