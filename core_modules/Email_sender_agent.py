import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from typing import Optional, Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Email Templates
EMAIL_TEMPLATES = {
    "invite": {
        "subject": "Interview Invitation - {company_name}",
        "body": """Dear {candidate_name},

We are pleased to inform you that your application for the {position} position at {company_name} has been shortlisted. We would like to invite you for an interview.

Interview Details:
Date: {interview_date}
Time: {interview_time}
Location: {interview_location}

Please confirm your attendance by replying to this email.

Best regards,
{company_name} HR Team"""
    },
    "rejection": {
        "subject": "Application Status Update - {company_name}",
        "body": """Dear {candidate_name},

Thank you for your interest in the {position} position at {company_name} and for taking the time to apply.

After careful consideration, we regret to inform you that we have decided to move forward with other candidates whose qualifications more closely match our current needs.

We appreciate your interest in {company_name} and wish you success in your job search.

Best regards,
{company_name} HR Team"""
    },
    "feedback": {
        "subject": "Application Feedback - {company_name}",
        "body": """Dear {candidate_name},

Thank you for your application for the {position} position at {company_name}.

{custom_feedback}

We appreciate your interest in {company_name} and wish you the best in your future endeavors.

Best regards,
{company_name} HR Team"""
    }
}

def get_email_content(status: str, template_data: Dict[str, str]) -> tuple:
    """
    Get email subject and body based on status and template data.
    
    Args:
        status (str): Email status type ('invite', 'rejection', or 'feedback')
        template_data (dict): Dictionary containing template variables
        
    Returns:
        tuple: (subject, body)
    """
    if status not in EMAIL_TEMPLATES:
        raise ValueError(f"Invalid status: {status}. Must be one of {list(EMAIL_TEMPLATES.keys())}")
    
    template = EMAIL_TEMPLATES[status]
    subject = template["subject"].format(**template_data)
    body = template["body"].format(**template_data)
    
    return subject, body

def send_email(
    id: str,
    email: str,
    status: str,
    template_data: Dict[str, str],
    smtp_server: str = "smtp.gmail.com",
    smtp_port: int = 587,
    sender_email: Optional[str] = None,
    sender_password: Optional[str] = None
) -> bool:
    """
    Send an email to a specified recipient with the given parameters.
    
    Args:
        id (str): Unique identifier for the email
        email (str): Recipient's email address
        status (str): Status of the email ('invite', 'rejection', or 'feedback')
        template_data (dict): Dictionary containing template variables
        smtp_server (str): SMTP server address (default: Gmail)
        smtp_port (int): SMTP server port (default: 587)
        sender_email (str, optional): Sender's email address
        sender_password (str, optional): Sender's email password or app password
        
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        # Get email content from template
        subject, body = get_email_content(status, template_data)
        
        # Create message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = email
        message["Subject"] = subject

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        # Create SMTP session
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Enable TLS
            if sender_email and sender_password:
                server.login(sender_email, sender_password)
            
            # Send email
            server.send_message(message)
            
        logger.info(f"Email sent successfully - ID: {id}, To: {email}, Status: {status}")
        return True

    except Exception as e:
        logger.error(f"Failed to send email - ID: {id}, Error: {str(e)}")
        return False

# # Example usage
# if __name__ == "__main__":
#     # Example template data
#     template_data = {
#         "candidate_name": "John Doe",
#         "company_name": "Tech Corp",
#         "position": "Software Engineer",
#         "interview_date": "2024-03-25",
#         "interview_time": "10:00 AM",
#         "interview_location": "Virtual Meeting",
#         "custom_feedback": "Your technical skills were impressive, but we're looking for someone with more experience in cloud technologies."
#     }
    
#     # Example: Send an invitation email
#     success = send_email(
#         id="12345",
#         email="rahul9392631467@gmail.com",
#         status="invite",
#         template_data=template_data,
#         sender_email="rahultejmora18@gmail.com",
#         sender_password="wcbo xeye rjie fatl"
#     )
    
#     if success:
#         print("Email sent successfully!")
#     else:
#         print("Failed to send email.")