from flask import render_template
from app import create_app, db
from flask_login import login_required

app = create_app()

with app.app_context():
    db.create_all()

@app.route('/')
@login_required
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
