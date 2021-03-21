import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash


def create_app(test_config=None):
    # create and configure the app

    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)



    from .models import db, User
    db.init_app(app)
    migrate = Migrate(app, db)
    
    @app.route('/sign_up', methods=('GET', 'POST'))
    def sign_up():
        if request.methode == 'POST':
            username = request.form['username']
            password = request.form['password']
            error = None

            if not username:
                error = 'Username is required'
            elif not password:
                error = 'Password is required'
            elif User.query.filtre_by(username=username).first():
                error = 'Username is already taken'


            if error is None:
                user = User(username=username, password=generate_password_hash(password))
                db.session.add(user)
                db.session.commit()
                flash("Successfully signed up! Please log in.", 'success')
                return redirect(url_for('log_in'))
            flash(error, 'error')
               
        return render_template('sign_up.html')

    @app.route('/log_in')
    def log_in():
         return render_template('log_in.html')

    return app
    # ensure the instance folder exists
#    try:
#        os.makedirs(app.instance_path)
#    except OSError:
#        pass

    # a simple page that says hello