from quart import Blueprint, render_template
from datastar_py.quart import ServerSentEventGenerator, make_datastar_response
import asyncio
import time
from datetime import datetime
from ..getdata import DataWrapper

__all__ = ["owl_bp"]

owl_bp = Blueprint("owl", __name__)

@owl_bp.route("/")
async def main():
    return await render_template("owl/main.html")

@owl_bp.route('/updates')
async def updates():
    fields = ["INDEX", "TIME", "NOISE", "STEPPY"]
    data = DataWrapper(fake=True)
    async def data_updates():
        while True:
            values = await data.wait_for_new_data(fields)
            response = {}
            for field in fields:
                key = f"field_{field.lower()}"
                if field.lower() == "time":
                    val = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(values[field]))
                else:
                    val = f"{values[field]:.02f}"
                response[key] = val
            yield ServerSentEventGenerator.merge_signals(response)

    response = await make_datastar_response(data_updates())
    return response
