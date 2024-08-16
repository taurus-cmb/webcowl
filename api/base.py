from flask import Flask, Blueprint, request
import os
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

api_bp = Blueprint("api", __name__)

def read_latest_data(fields):
    """Read the latest values of data from a dirfile"""
    import pygetdata as gd
    response = dict()
    df = gd.dirfile(app.config["DATA_PATH"])
    eof = df.nframes - 1
    response["INDEX"] = eof
    for field in fields:
        # INDEX handled separately
        if field == "INDEX":
            continue
        try:
            response[field] = df.getdata(field, first_frame=eof, num_frames=1)[-1]
        except gd.BadCodeError:
            # leave requests for non-existent fields blank
            continue
    return response

# a bit of a hack to import from parent folder
if app.config["FAKE_DATA"]:
    import sys
    base_dir = app.config["BASE_DIR"]
    sys.path.append(base_dir)

def fake_latest_data(fields):
    """Simulate some fake data for testing, rather than reading from dirfile"""
    from data_faker import get_fake_data
    return get_fake_data(fields)

@api_bp.route('/latest', methods=["POST"])
def latest_data():
    fields = request.json["fields"]
    if not app.config["FAKE_DATA"]:
        return read_latest_data(fields)
    else:
        return fake_latest_data(fields)


# this must happen after the routes are declared
app.register_blueprint(api_bp, url_prefix="/api")
