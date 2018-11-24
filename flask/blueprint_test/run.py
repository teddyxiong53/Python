from app import app
from app.dept import dept
from app.user import user

app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(dept, url_prefix='/dept')

app.run(host="0.0.0.0", port=9090)


