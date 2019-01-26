from flask import Flask, redirect, url_for
import os
from code import basicbits
def create_app():
    app = Flask(__name__)
    app.register_blueprint(basicbits.bp)
    @app.route('/')
    def index():
        return redirect(url_for('basicbits.render_home'))
    return app
app = create_app()
app.run(port=5050)
