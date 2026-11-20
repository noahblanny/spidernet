"""Read-only local Flask dashboard."""
from flask import Flask, render_template
from .storage import initialize, list_devices, list_scans

def create_app():
    app = Flask(__name__)

    @app.get("/")
    def index():
        initialize()
        devices = list_devices()
        scans = list_scans()
        return render_template("index.html", devices=devices, scans=scans,
                               known=sum(bool(d["known"]) for d in devices))

    return app
