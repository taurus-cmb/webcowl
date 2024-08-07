from flask import Flask, Blueprint, request
import pygetdata as gd
import os

app = Flask(__name__)

api_bp = Blueprint("api", __name__)

@api_bp.route('/latest', methods=["POST"])
def latest_data():
    response = dict()

    # TODO make dirfile path a config variable
    # TODO make dirfile not open every time?
    dirfile_path = os.path.join(os.path.dirname(__file__), os.pardir, "fake_data")
    df = gd.dirfile(dirfile_path)

    eof = df.nframes - 1
    response["INDEX"] = eof
    fields = request.json["fields"]
    for field in request.json["fields"]:
        # INDEX handled separately
        if field == "INDEX":
            continue
        try:
            response[field] = df.getdata(field, first_frame=eof, num_frames=1)[-1]
        except gd.BadCodeError:
            # leave requests for non-existent fields blank
            continue

    return response


# this must happen after the routes are declared
app.register_blueprint(api_bp, url_prefix="/api")
