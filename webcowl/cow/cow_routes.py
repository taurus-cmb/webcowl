from quart import Blueprint, helpers, current_app, render_template
from datastar_py.quart import ServerSentEventGenerator, make_datastar_response
import asyncio
from pyface.proto_cmd import ProtoCmd, ProtoCmdError
from ..session_resource import SessionResource

__all__ = ["cow_bp"]

cow_bp = Blueprint("cow", __name__)

protocmd_pool = None

def _get_protocmd():
    global protocmd_pool
    if protocmd_pool is None:
        protocmd_pool = SessionResource(
            ProtoCmd,
            current_app.config["COW_INFO_PORT"],
            current_app.config["COW_ROOT_MESSAGE"],
            current_app.config["COW_COMMAND_PORT"],
        )
    return protocmd_pool.get_resource()


@cow_bp.route("/")
async def main():
    return await render_template("cow/main.html")

@cow_bp.route("/set_command/<path:cmd_path>", methods=["GET", "POST"])
async def set_command(cmd_path):
    cmd_split = cmd_path.split("/")
    # remove empty segments from extra /
    cmd_split = [c for c in cmd_split if len(c) > 0]
    _get_protocmd().set_active_command(cmd_split)
    return ""

# extra route to handle empty (home) path
# TODO maybe use the data of the post, rather than its route?
@cow_bp.route("/set_command/", methods=["GET", "POST"])
async def set_command_home():
    return await set_command("")

@cow_bp.route('/updates')
async def updates():
    local_cmd = _get_protocmd()

    @helpers.stream_with_context
    async def data_updates():
        while True:
            if current_app.shutdown_event.is_set():
                return
            update = await render_template(
                "cow/_command.html", **local_cmd.render_message_view("State")
            )
            yield ServerSentEventGenerator.merge_fragments(update)
            await asyncio.sleep(0.5)

    response = await make_datastar_response(data_updates())
    return response
