from db import db
from flask import request, url_for

from utils.mailgun import Mailgun


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    activated = db.Column(db.Boolean)

    def __init__(self, username, email, password, activated=False):
        self.username = username
        self.email = email
        self.password = password
        self.activated = activated

    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'activated': self.activated
        }

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def send_confirmation_email(self):
        subject = 'Registration Confirmation'
        link = request.url_root[:-1] + url_for("userconfirm", _id=self.id)
        text = f'Please click the link to confirm: {link}'
        html = f'<html>Confirm your registration <a href={link}>here</a></html>'
        return Mailgun.send_email(self.email, subject, text, html)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
