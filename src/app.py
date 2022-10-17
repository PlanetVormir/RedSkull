from flask import Flask, request
from scraper_lib import RedSkull

app = Flask(__name__)
api = RedSkull()


@app.route("/search", methods=["GET"])
def search():
    args = request.args

    if "keyword" not in args.keys():
        return {"error": "keyword is a required parameter"}, 422

    return api.search(args.get("keyword"), args.get("page_no", 1))


@app.route("/movies", methods=["GET"])
def movies():
    args = request.args

    if "media_id" not in args.keys():
        return {"error": "media_id is a required parameter"}, 422

    return api.movie(args["media_id"])


@app.route("/series", methods=["GET"])
def series():
    args = request.args

    if "media_id" not in args.keys():
        return {"error": "media_id is a required parameter"}, 422

    return api.series(args["media_id"])


@app.route("/episode", methods=["GET"])
def episode():
    args = request.args

    if "episode_id" not in args.keys():
        return {"error": "episode_id is a required parameter"}, 422

    return api.episode(args["episode_id"])


if __name__ == "__main__":
    app.run(debug=True)
