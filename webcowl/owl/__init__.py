from quart import Blueprint, render_template

__all__ = ["owl_bp"]

owl_bp = Blueprint("owl", __name__)

@owl_bp.route("/")
async def main():
    return await render_template("owl/main.html")

# @owl_bp.route('/latest', methods=["POST"])
# async def latest_data():
#     fields = request.json["fields"]
#     if not app.config["FAKE_DATA"]:
#         return read_latest_data(fields)
#     else:
#         return fake_latest_data(fields)
