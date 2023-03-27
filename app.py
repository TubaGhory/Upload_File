import random
import os
from flask import Flask, request, jsonify 
from pydub import AudioSegment
import soundfile as sf
import requests

URL = "https://boldly-ideal-owl-fort-dev.wayscript.cloud/predict"
FILE_PATH="./output_audio.wav"

app = Flask(__name__)

@app.route("/convert",methods=["POST"])

def convert():
    if os.path.exists("output_audio.wav"):
        os.remove("output_audio.wav")
    audio_file=request.files["file"]
    file_name = str(random.randint(0,100000))+".wav"
    audio_file.save(file_name)

    os.system("ffmpeg -i "+file_name+" output_audio.wav")

    # open files
    file = open(FILE_PATH, "rb")
    # package stuff to send and perform POST request
    values = {"file": (FILE_PATH, file, "audio/wav")}
    response = requests.post(URL, files=values)
    data = response.json()

    print("Predicted keyword: {}".format(data["keyword"]))

    os.remove(file_name)
    return data["keyword"]

if __name__ == "__main__":
    app.run(debug = False,host="0.0.0.0")