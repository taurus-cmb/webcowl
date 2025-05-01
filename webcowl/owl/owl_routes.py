from quart import Blueprint, render_template
from datastar_py.quart import ServerSentEventGenerator, make_datastar_response
import asyncio
import os
import time
from datetime import datetime
from ..getdata import DataWrapper
from .owl_renderer import OwlRenderer

__all__ = ["owl_bp"]

owl_bp = Blueprint("owl", __name__)

# TODO make the owl config not just fixed/hardcoded
path = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "examples", "example_owl_config.yml")
owl_renderer = OwlRenderer(path)

@owl_bp.route("/")
async def main():
    return await owl_renderer.clone().render_template()

@owl_bp.route('/updates')
async def updates():
    local_renderer = owl_renderer.clone()
    async def data_updates():
        while True:
            update = await local_renderer.wait_and_render_signal_updates()
            yield ServerSentEventGenerator.merge_signals(update)

    response = await make_datastar_response(data_updates())
    return response
