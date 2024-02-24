import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(sender_email, receiver_email, subject, message, smtp_server, smtp_port, smtp_username, smtp_password):
    # Създаване на обект за изпращане на имейл
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Добавяне на текст към имейла
    msg.attach(MIMEText(message, 'plain'))

    # Изпращане на имейла
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # Започване на комуникация с SMTP сървъра
            server.starttls()

            # Влизане с потребителско име и парола, ако е необходимо
            server.login(smtp_username, smtp_password)

            # Изпращане на имейла
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Имейлът беше успешно изпратен.")

    except Exception as e:
        print("Грешка при изпращане на имейл:", str(e))


# Пример на използване на функцията
sender_email = "your_email@gmail.com"
receiver_email = "recipient_email@example.com"
subject = "Тестов имейл"
message = "Това е тестов имейл, изпратен от Python."

smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = "your_email@gmail.com"
smtp_password = "your_email_password"

send_email(sender_email, receiver_email, subject, message, smtp_server, smtp_port, smtp_username, smtp_password)
