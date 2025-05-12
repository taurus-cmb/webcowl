from quart import Blueprint, helpers, current_app, render_template, stream_with_context, request
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

async def _render_cow_command_view(app):
    async with app.app_context():
        local_cmd = _get_protocmd()
        @stream_with_context
        async def sse_update():
            update = await render_template(
                "cow/_command.html", **local_cmd.render_message_view("State")
            )
            yield ServerSentEventGenerator.merge_fragments(update)

        return await make_datastar_response(sse_update())

@cow_bp.route("/set_command/<path:cmd_path>", methods=["POST"])
async def set_command(cmd_path):
    cmd_split = cmd_path.split("/")
    # remove empty segments from extra /
    cmd_split = [c for c in cmd_split if len(c) > 0]
    _get_protocmd().set_active_command(cmd_split)
    return await _render_cow_command_view(current_app)

# extra route to handle empty (home) path
# TODO maybe use the data of the post, rather than its route?
@cow_bp.route("/set_command/", methods=["POST"])
async def set_command_home():
    return await set_command("")

ERR_PREFIX = "_error_"

@cow_bp.route("/update_field", methods=["POST"])
# TODO could move most of this code to proto_cmd, if desired
async def update_field():
    json = await request.json
    local_cmd = _get_protocmd()
    remove = []
    errors = {}
    active_path = "/".join(local_cmd.active_path)
    for signal, value in json.items():
        path = signal.replace(local_cmd.signal_sep, "/")
        errkey = ERR_PREFIX + signal
        if not path.startswith(active_path):
            remove.append(signal)
        elif len(value) == 0:
            # reset errors for empty fields
            errors[errkey] = ""
        else:
            try:
                # TODO make things consistent between lists and /
                local_cmd.update_field(path.split("/"), value)
                errors[errkey] = ""
            except ProtoCmdError as e:
                errors[errkey] = "ERROR: " + str(e)

    async def command_signal_update():
        yield ServerSentEventGenerator.remove_signals(remove)
        yield ServerSentEventGenerator.merge_signals(errors)

    return await make_datastar_response(command_signal_update())

# route to load the commands when the page is first visited
# TODO is it better to do this all as part of the initial page render?
@cow_bp.route('/load')
async def updates():
    return await _render_cow_command_view(current_app)
