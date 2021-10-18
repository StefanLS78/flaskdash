# Flask-Migrate gives more control over dbase, for future updates
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import app, current_app, Blueprint
from flask_login import UserMixin, current_user
from flask_bcrypt import Bcrypt
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.sql.schema import ForeignKey, MetaData
from flaskapp import db, login_manager, bcrypt


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


user_roles = db.Table('user_roles',
                      db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                      db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
                      )


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=False)

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(), nullable=False, default='default.jpg')
    password = db.Column(db.String(),
                         nullable=False)  # bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    roles = db.relationship('Role', secondary=user_roles, lazy='joined')

    # role_name = db.Column(db.String, db.ForeignKey('role.name'))

    # def __init__ (self, image_file=None, username=None, email=None):
    #     self.data = (image_file, username, email)

    # def is_active(self):
    #     return True    

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

# class UserRoles(db.Model):
#     __tablename__ = 'user_roles'
#     id = db.Column(db.Integer(), primary_key=True)
#     user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
#     roles_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

#     def __str__(self):
#         return self.name


# @app.before_first_request
# def create_superuser():
#     db.create_all()
#     if not User.query.filter(User.email =='superuser@example.com').first():
#         user1 = User(
#                 username='superuser', 
#                 email='superuser@example.com',
#                 password= bcrypt.generate_password_hash('SuperSecret1').decode('utf-8'),
#                 )
#         user1.roles.append(Role(name='admin'))
#         db.session.add(user1)
#         db.session.commit()
