from quart import Blueprint, helpers, current_app, render_template
from datastar_py.quart import ServerSentEventGenerator, make_datastar_response
import time
import asyncio

__all__ = ["cow_bp"]

cow_bp = Blueprint("cow", __name__)

@cow_bp.route("/")
async def main():
    return await render_template("cow/main.html")

@cow_bp.route('/updates')
async def updates():

    @helpers.stream_with_context
    async def data_updates():
        while True:
            if current_app.shutdown_event.is_set():
                return
            update = f"""<span id="cow-time">Update: {time.time():.2f}"""
            print("Updating:", update)
            yield ServerSentEventGenerator.merge_fragments(update)
            await asyncio.sleep(0.5)

    response = await make_datastar_response(data_updates())
    return response
