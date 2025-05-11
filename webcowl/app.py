from quart import Quart, render_template
from .owl import owl_bp
from .cow import cow_bp
from .config import Config
import asyncio
import signal

app = Quart(__name__)

app.config.from_object(Config)

app.register_blueprint(owl_bp, url_prefix="/owl")
app.register_blueprint(cow_bp, url_prefix="/cow")

@app.route("/")
async def home():
    return await render_template("home.html")

# manually implement an Event for shutting down streaming response generators
# this is lifted from the version not working in quart/app.py
# Streaming generators should return when: current_app.shutdown_event.is_set()
app.shutdown_event = asyncio.Event()

def _signal_handler(*_):
    app.shutdown_event.set()

for signal_name in {"SIGINT", "SIGTERM", "SIGBREAK"}:
    if hasattr(signal, signal_name):
        signal.signal(getattr(signal, signal_name), _signal_handler)


#app.run()
