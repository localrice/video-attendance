from flask import request, render_template
from app.services.settings_service import load_settings, save_settings


def settings_route():
    if request.method == "GET":
        settings = load_settings()
        return render_template("settings.html", settings=settings)
    
    data = {
        "resize_scale": float(request.form["resize_scale"]),
        "process_fps": int(request.form["process_fps"]),
        "match_threshold": float(request.form["match_threshold"])
    }

    save_settings(data)
    return render_template("settings.html", settings=data, message="Saved")