from flask import render_template

from . import blueprint


@blueprint.route("/", methods=["GET"])
def index():
    return render_template("transactions/index.html")