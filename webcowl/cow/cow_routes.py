from quart import Blueprint, helpers, current_app, render_template
from datastar_py.quart import ServerSentEventGenerator, make_datastar_response
import asyncio
from pyface.proto_cmd import ProtoCmd, ProtoCmdError

__all__ = ["cow_bp"]

cow_bp = Blueprint("cow", __name__)

root_message = "system.HKsystem"

command_port = ("127.0.0.1", 3006)
info_port = ("127.0.0.1", 3007)
print("info port", info_port)

protocmd = ProtoCmd(info_port, root_message, command_port)
current_cmd = []
#update_event = asyncio.Event()


@cow_bp.route("/")
async def main():
    return await render_template("cow/main.html")

@cow_bp.route("/set_command/<path:cmd_path>", methods=["GET", "POST"])
async def set_command(cmd_path):
    print("setting command to:", cmd_path)
    global current_cmd, update_event
    current_cmd = cmd_path.split("/")
    print("setting command to:", current_cmd)
    # remove empty segments from extra /
    current_cmd = [c for c in current_cmd if len(c) > 0]
    #update_event.set()
    return ""

# extra route to handle empty (home) path
# TODO maybe use the data of the post, rather than its route?
@cow_bp.route("/set_command/", methods=["GET", "POST"])
async def set_command_home():
    return await set_command("")

@cow_bp.route('/updates')
async def updates():

    @helpers.stream_with_context
    async def data_updates():
        while True:
            if current_app.shutdown_event.is_set():
                return
            update = await render_template(
                "cow/_command.html", **protocmd.render_message_view("State", current_cmd)
            )
            yield ServerSentEventGenerator.merge_fragments(update)
            await asyncio.sleep(0.5)

    response = await make_datastar_response(data_updates())
    return response
