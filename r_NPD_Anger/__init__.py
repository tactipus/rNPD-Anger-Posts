import os
from r_NPD_Anger.database import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import cast, Integer, desc


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'r_NPD_Anger.sqlite'),
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/pnalzate/Documents/GitHub' \
                                            '/rNPD-Anger-Posts/instance/r_NPD_Anger.sqlite'
    db = SQLAlchemy(app)

    db.Model.metadata.reflect(db.engine)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    @app.route('/home')
    def home():
        return 'This is my Flask project! I will be adding more to this as the site grows. It\'s' \
               'main use right now is to view certain posts from r/NPD.'

    database.init_app(app)

    from r_NPD_Anger import NPD_anger_posts
    from flask import (
        Blueprint, render_template, request
    )

    class Post(db.Model):
        __table__ = db.Model.metadata.tables['posts']

    ROWS_PER_PAGE = 20

    @app.route('/narcissism_project', methods=['GET'])
    def angry_posts():
        page = request.args.get('page', 1, type=int)
        posts = Post.query.order_by(desc(cast(Post.comms_num, Integer))).paginate(page=page, per_page=ROWS_PER_PAGE)

        return render_template('narcissism_project.html', posts=posts)

    return app
