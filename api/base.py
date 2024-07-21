from flask import Flask
import pygetdata as gd
import os

api = Flask(__name__)

@api.route('/test')
def test_data():
    response = dict()

    # TODO make dirfile path a config variable
    # TODO make dirfile not open every time?
    dirfile_path = os.path.join(os.path.dirname(__file__), os.pardir, "fake_data")
    df = gd.dirfile(dirfile_path)

    # TODO include fields to read in a POST request
    eof = df.nframes - 1
    for field in ["TIME", "NOISE", "STEPPY"]:
        response[field] = df.getdata(field, first_frame=eof, num_frames=1)[-1]
    response["frame"] = eof

    return response
