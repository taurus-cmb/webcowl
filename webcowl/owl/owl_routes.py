from quart import Blueprint, helpers, current_app
from datastar_py.quart import ServerSentEventGenerator, make_datastar_response
import os
from .owl_renderer import OwlRenderer
from ..session_resource import SessionResource

__all__ = ["owl_bp"]

owl_bp = Blueprint("owl", __name__)

owl_renderers = None

def _get_renderer():
    global owl_renderers
    if owl_renderers is None:
        owl_renderers = SessionResource(OwlRenderer, current_app.config["OWL_FILE"])
    return owl_renderers.get_resource()

@owl_bp.route("/")
async def main():
    local_renderer = _get_renderer()
    return await local_renderer.render_template()

@owl_bp.route('/updates')
async def updates():
    local_renderer = _get_renderer()

    @helpers.stream_with_context
    async def data_updates():
        while True:
            if current_app.shutdown_event.is_set():
                return
            update = await local_renderer.wait_and_render_signal_updates(timeout=1)
            yield ServerSentEventGenerator.merge_signals(update)

    response = await make_datastar_response(data_updates())
    return response
