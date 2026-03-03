import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

FROM_EMAIL = os.getenv("FROM_EMAIL")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

def catching_users(cursor):
    cursor.execute("SELECT * FROM users.users")
    results = cursor.fetchall()
    return results

def define_body(news_summary):
    news = ""
    for new in news_summary:
        new = f"""
            <h3>{new["title"]}</h3>
            <p>{new["summary"]}</p>
            <hr/>
        """
        news = news + new
    return news

def SendEmail(news_summary, cursor, log):
    log.info = "Catching users"
    users = catching_users(cursor)
    body_message = define_body(news_summary)

    for user in users:
        name = "{} {}".format(user[1], user[2])
        email = user[3]

        msg = MIMEMultipart()
        msg["From"] = FROM_EMAIL
        msg["To"] = email
        msg["Subject"] = f"Novidades Exclusivas para Você, {name}"
        msg.add_header('Content-Type', 'text/html')

        msg.attach(MIMEText(body_message, 'html'))

        with smtplib.SMTP("smtp.sendgrid.net", 587) as server:
            server.starttls()
            server.login("apikey", SENDGRID_API_KEY)
            server.send_message(msg)
            server.quit()
    log.info = "Email sent successfully"
    
        
    

