from flask import Flask
from app.routes.index import index_route
from app.routes.enroll import enroll_route
from app.services.db_service import init_db
from app.routes.attendance import attendance_route
from app.routes.settings import settings_route

init_db()
app = Flask(__name__, template_folder="app/templates")

app.add_url_rule("/", view_func=index_route, methods=["GET"])
app.add_url_rule("/enroll", view_func=enroll_route, methods=["GET", "POST"])
app.add_url_rule("/attendance", view_func=attendance_route, methods=["GET", "POST"])
app.add_url_rule("/settings", view_func=settings_route, methods=["GET", "POST"])

if __name__ == "__main__":
    app.run(debug=True)