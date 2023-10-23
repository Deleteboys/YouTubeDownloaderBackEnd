from pytube import YouTube
from flask import Flask, jsonify, make_response, request, flash, redirect, url_for
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/videoInfo', methods=['POST'])
def get_video_infos():
    data = request.json
    if 'video' in data:
        yt = YouTube(data['video'])
        title = yt.title
        thumbnail_url = yt.thumbnail_url
        input_streams_mp4 = yt.streams.filter(file_extension='mp4').order_by('resolution')
        input_streams_mp3 = yt.streams.filter(file_extension='mp4').order_by('abr')
        mp4_resolutions = ["MP4("+stream.resolution+")" for stream in input_streams_mp4.fmt_streams if stream.mime_type == "video/mp4"]
        mp3_resolutions = ["MP3("+stream.abr+")" for stream in input_streams_mp3.fmt_streams]

        output = {
            "title": title,
            "thumbnail": thumbnail_url,
            "mp4": mp4_resolutions,
            "mp3": mp3_resolutions
        }

        return output
    else:
        return "Error", 400



if __name__ == '__main__':
    app.run(debug=True)
    # print(YouTube('https://youtu.be/9bZkp7q19f0').thumbnail_url)
    # print(YouTube('https://youtu.be/9bZkp7q19f0').title)
    # print(YouTube('https://youtu.be/9bZkp7q19f0').streams.filter(file_extension='mp4').order_by('resolution').fmt_streams[0].download())
    # print(YouTube('https://youtu.be/9bZkp7q19f0').streams.filter(only_audio=True).order_by('abr'))
