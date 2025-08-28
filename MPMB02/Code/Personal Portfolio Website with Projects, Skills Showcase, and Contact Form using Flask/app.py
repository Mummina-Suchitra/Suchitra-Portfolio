from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime
from forms import ContactForm
import os

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///portfolio.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Mail configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

# Initialize extensions
db = SQLAlchemy(app)
mail = Mail(app)

# Models
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contact(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data
        )
        db.session.add(contact)
        db.session.commit()

        # Send email notification
        try:
            msg = Message(
                subject=f'New Contact Form Submission: {form.subject.data}',
                sender=app.config['MAIL_USERNAME'],
                recipients=[app.config['MAIL_USERNAME']]
            )
            msg.body = f"""New contact form submission:
            Name: {form.name.data}
            Email: {form.email.data}
            Subject: {form.subject.data}
            Message: {form.message.data}"""
            mail.send(msg)
            flash('Your message has been sent successfully!', 'success')
        except Exception as e:
            flash('Your message was saved but email notification failed.', 'warning')

        return redirect(url_for('index'))

    projects = [
        {
            'title': 'Project 1',
            'description': 'This project implements real-time eye detection using OpenCV and a Haar Cascade classifier. It captures video from the webcam, processes each frame to detect eyes, and highlights them with green rectangles. This program can be useful for eye-tracking applications, gaze detection, and basic computer vision projects.',
            'image': 'project1.jpg',
            'technologies': ['Python', 'Flask', 'SQLAlchemy']
        },
        {
            'title': 'Project 2',
            'description': 'This project is a responsive and feature-rich calculator application designed to perform basic arithmetic operations and advanced mathematical computations. Built with a modern tech stack, it ensures a seamless user experience and efficient performance.',
            'image': 'project2.jpg',
            'technologies': ['JavaScript', 'React', 'Node.js']
        }
    ]
    
    skills = {
        'Programming Languages': ['Python', 'JavaScript', 'Java', ],
        'Web Technologies': ['HTML5', 'CSS3', 'React', 'Vue.js'],
        'Databases': ['MySQL', 'PostgreSQL', 'MongoDB'],
        'Tools': ['Git', 'Docker', 'AWS']
    }
    
    return render_template('index.html', form=form, projects=projects, skills=skills)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)