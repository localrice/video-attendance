from flask import Flask
from app.routes.enroll import enroll_route
from app.services.db_service import init_db

init_db()
app = Flask(__name__, template_folder="app/templates")

app.add_url_rule("/", view_func=enroll_route, methods=["GET", "POST"])
if __name__ == "__main__":
    app.run(debug=True)