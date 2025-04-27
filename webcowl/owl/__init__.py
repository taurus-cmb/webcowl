from quart import Blueprint, render_template
from datastar_py.quart import ServerSentEventGenerator, make_datastar_response
import asyncio
from datetime import datetime

__all__ = ["owl_bp"]

owl_bp = Blueprint("owl", __name__)

@owl_bp.route("/")
async def main():
    return await render_template("owl/main.html")

@owl_bp.route('/updates')
async def updates():
    async def time_updates():
        while True:
            yield ServerSentEventGenerator.merge_signals({"field_time": f"{datetime.now().isoformat()}"})
            await asyncio.sleep(1)

    response = await make_datastar_response(time_updates())
    return response
    # fields = request.json["fields"]
    # if not app.config["FAKE_DATA"]:
    #     return read_latest_data(fields)
    # else:
    #     return fake_latest_data(fields)
