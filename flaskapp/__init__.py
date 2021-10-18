from flask import Flask, redirect
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required, current_user
from flask_mail import Mail
from flask_admin import Admin, AdminIndexView

db = SQLAlchemy()
admin = Admin()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


# #############################==========----- Flask app / Dash app -----==========##############################

def init_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # #############################==========----- app context / Blueprint sectie -----==========##########################

    with app.app_context():
        from flaskapp.users.routes import users
        from flaskapp.main.routes import main
        from flaskapp.commander.routes import commander
        from flaskapp.errors.handlers import errors
        from flaskapp.beheer import beheer
        app.register_blueprint(users)
        app.register_blueprint(main)
        app.register_blueprint(commander)
        app.register_blueprint(errors)
        app.register_blueprint(beheer)

        # #############################==========----- Dashapp protection -----==========##############################

        from flaskapp.dashapp.dashboard import init_dashboard
        app = init_dashboard(app)

        # for view_func in app.server.view_functions:
        #     if view_func.startswith('/dashboard/'):
        #         app.server.view_functions[view_func] = login_required(app.server.view_functions[view_func])

        # #############################==========----- superuser initialization -----==========##############################

        from flaskapp.models import User, Role

        @app.before_first_request
        def create_superuser():
            db.create_all()
            if not User.query.filter(User.email == 'superuser@example.com').first():
                user1 = User(
                    username='superuser',
                    email='superuser@example.com',
                    password=bcrypt.generate_password_hash('SuperSecret1').decode('utf-8')
                )
                user1.roles.append(Role(name='admin'))
                db.session.add(user1)
                db.session.commit()

# #############################==========----- admin initialization -----==========##############################
        from flaskapp.models import User

        class Controller(AdminIndexView):  # admin security
            def is_accessible(self):
                if current_user.is_authenticated:
                    return True

            #     if not current_user.is_active or not current_user.is_authenticated:
            #         return 403
            #
            #     if current_user.hasattr(User.roles, 'admin'):  # "1" is the administrator ID in the site.db
            #         # database.
            #         return True  # So, if user has 1 (admin) (s)he can acces the adminpanel
            #
            #     return 403
            #
            # def inaccessible_callback(self, name, **kwargs):
            #     return redirect(url_for('users.login'))

        admin.init_app(app, index_view=Controller())  # initialization of admin section

# #############################==========----- return app -----==========##############################

    return app
