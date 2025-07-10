import os

from flask import current_app
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Content, Email, Mail, To


def send_email(to_email: str, subject: str, html_content: str) -> bool:
    """Send an email using SendGrid API.

    Args:
        to_email (str): Recipient's email address
        subject (str): Email subject
        html_content (str): HTML content of the email

    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        from_email = Email(os.getenv('SENDGRID_FROM_EMAIL'))
        recipient_email = To(to_email)
        content = Content("text/html", html_content)
        mail = Mail(from_email, recipient_email, subject, content)
        sg.send(mail)
        current_app.logger.info(f"Email sent successfully to {to_email}")
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to send email: {str(e)}")
        return False


def send_reset_password_email(to_email: str, reset_token: str) -> bool:
    """Send a password reset email using SendGrid API.

    Args:
        to_email (str): Recipient's email address
        reset_token (str): Password reset token

    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    frontend_url = os.getenv('FRONTEND_URL')
    reset_url = f"{frontend_url}/reset-password?token={reset_token}"
    subject = "Password Reset Request"
    html_content = f"""
    <html>
        <body>
            <h2>Password Reset Request</h2>
            <p>You have requested to reset your password.
            Click the link below to proceed:</p>
            <p><a href="{reset_url}">Reset Password</a></p>
            <p>If you did not request this, please ignore this email.</p>
            <p>This link will expire in 1 hour.</p>
        </body>
    </html>
    """
    return send_email(to_email, subject, html_content)
