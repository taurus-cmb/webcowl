from quart import Quart, render_template
from .owl import owl_bp
import os
# TODO config
#from config import Config

app = Quart(__name__)
# TODO config
#app.config.from_object(Config)
app.register_blueprint(owl_bp, url_prefix="/owl")

@app.route("/")
async def home():
    return await render_template("home.html")

app.run()
