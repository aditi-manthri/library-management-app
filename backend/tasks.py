import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import csv
from io import StringIO
from datetime import datetime, timedelta
from celery_config import celery
from app import app, User, Book, Read
from celery.schedules import crontab
from sqlalchemy import extract


@celery.task
def daily_user_reminder():
        with app.app_context():
            yesterday = datetime.now() - timedelta(days=1)
            users = User.query.filter(User.last_login <= yesterday).all()
            if users:
                for user in users:
                    subject = 'We miss you!'
                    html_content = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>We miss you!</title>
                    </head>
                    <body>
                        <h1>Hello {user.username},</h1>
                        <p>We noticed that you haven't logged in all day. We miss you!Please take the time to log in today.</p>
                        <p>Thank you,</p>
                        <p>The Readr Team</p>
                    </body>
                    </html>
                    """
                send_email(user.email, html_content, subject)

@celery.task                
def generate_monthly_report():
    with app.app_context():
        current_month = datetime.now().month
        current_year = datetime.now().year

        users = User.query.all()
        for user in users:
            reads = Read.query.filter_by(user_id=user.id).filter(extract('year', Read.timestamp) == current_year, extract('month', Read.timestamp) == current_month).all()
            num_books_read = len(reads)

            subject = 'Monthly Activity Report'
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Monthly Activity Report</title>
            </head>
            <body>
                <h1>Hello, {user.username},</h1>
                <h1>Monthly Report - {datetime.now().strftime('%B')} {current_year} </h1>
                <p>You read {num_books_read} books this month. Great job! All the best for next month.</p>
                <p>Thank you,</p>
                <p>The Readr Team</p>
            </body>
            </html>
            """
            send_email(user.email, html_content, subject)

def send_email(to_email, html_content, subject):
    from_email="admin@readr.com"
    #to_email = user.email
    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    part1 = MIMEText(html_content, 'html')
    msg.attach(part1)

    smtp_server = 'localhost'
    smtp_port = 1025

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.send_message(msg)