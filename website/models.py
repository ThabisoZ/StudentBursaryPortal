from . import db
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    sponsored_opportunities = db.relationship('Opportunity')

class Opportunity(db.Model):
    __tablename__ = 'opportunity'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False)  # Type of opportunity (e.g., bursary, scholarship, grant, internship, learnership etc.)
    deadline = db.Column(db.DateTime, nullable=True)
    location = db.Column(db.String(100), nullable=True)

    sponsor_id = db.Column(db.Integer, db.ForeignKey('user.id'),)
    sponsor = db.relationship('User',)
    
class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunity.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    applied_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    #document = db.Column(db.LargeBinary)
    #qualifications = db.Column(db.LargeBinary)
    #metric_certificate = db.Column(db.LargeBinary)
    #proof_of_registration = db.Column(db.LargeBinary)
    #proof_of_income = db.Column(db.LargeBinary)
    #Cover_Letter=db.column(db.LargeBinary)

    opportunity = db.relationship('Opportunity')
    user = db.relationship('User')



class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)

    sender = db.relationship('User', foreign_keys=[sender_id], backref=db.backref('sent_messages', lazy=True))
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref=db.backref('received_messages', lazy=True))


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now)

    user = db.relationship('User', backref=db.backref('reviews', lazy=True))


class UrgentHelp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    note = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship('User')
 
