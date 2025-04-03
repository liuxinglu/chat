from flask import render_template
from app import create_app,db
from flask_login import login_required
from waitress import serve
import logging
from werkzeug.middleware.proxy_fix import ProxyFix

app = create_app()
with app.app_context():
    db.create_all()

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)


@app.route('/')
@login_required
def index():
    return render_template('index1.html')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve(app, host='0.0.0.0', port=5000)

