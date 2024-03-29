from sqlalchemy.orm import synonym
from werkzeug import check_password_hash, generate_password_hash
from datetime import datetime

from board_app import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), default='', nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    _password = db.Column('password', db.String(100), nullable=False)

    def _get_password(self):
        return self._password
    def _set_password(self, password):
        if password:
            password = password.strip()
        self._password = generate_password_hash(password)
    password_descriptor = property(_get_password, _set_password)
    password = synonym('_password', descriptor=password_descriptor)

    def check_password(self, password):
        password = password.strip()
        if not password:
            return False
        return check_password_hash(self.password, password)

    @classmethod
    def authenticate(cls, query, email, password):
        user = query(cls).filter(cls.email==email).first()
        if user is None:
            return None, False
        return user, user.check_password(password)

    def __repr__(self):
        return u'<User id={self.id} email={self.email!r}>'.format(
                self=self)


class Entry(db.Model):
    __tablename__ = 'entries'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    text = db.Column(db.Text)
    name = db.Column(db.String(100))
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Entry id={id} title={title!r}>'.format(
                id=self.id, title=self.title, name = self.name, pub_date = self.pub_date)

def init():
    db.create_all()
