from flask import render_template
from app import create_app,db
from flask_login import login_required
from waitress import serve
import logging

app = create_app()
with app.app_context():
    db.create_all()

@app.route('/')
@login_required
def index():
    return render_template('index1.html')

if __name__ == '__main__':
    # app.run(debug=True, port=5000)
    logging.basicConfig(level=logging.DEBUG)
    serve(app, host='0.0.0.0', port=5000)

