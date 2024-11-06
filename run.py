from flask import render_template
from app import create_app
import os

app = create_app()


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.secret_key = os.urandom(24).hex()
    app.run(debug=True)
