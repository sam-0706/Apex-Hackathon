from .Email_sender_agent import send_email, EMAIL_TEMPLATES
from typing import Dict
import logging

logger = logging.getLogger(__name__)


def send_invitation_email(
    sender_email: str,
    sender_password: str,
    candidate_email: str,
    candidate_name: str,
    position: str,
    interview_date: str,
    interview_time: str,
    interview_location: str,
    company_name: str = "Our Company"
) -> bool:
    """
    Send an interview invitation email.
    """
    template_data = {
        "candidate_name": candidate_name,
        "company_name": company_name,
        "position": position,
        "interview_date": interview_date,
        "interview_time": interview_time,
        "interview_location": interview_location
    }

    return send_email(
        id=f"invite_{candidate_email}",
        email=candidate_email,
        status="invite",
        template_data=template_data,
        sender_email=sender_email,
        sender_password=sender_password
    )


def send_rejection_email(
    sender_email: str,
    sender_password: str,
    candidate_email: str,
    candidate_name: str,
    position: str,
    company_name: str = "Our Company"
) -> bool:
    """
    Send a rejection email.
    """
    template_data = {
        "candidate_name": candidate_name,
        "company_name": company_name,
        "position": position
    }

    return send_email(
        id=f"reject_{candidate_email}",
        email=candidate_email,
        status="rejection",
        template_data=template_data,
        sender_email=sender_email,
        sender_password=sender_password
    )


def send_feedback_email(
    sender_email: str,
    sender_password: str,
    candidate_email: str,
    candidate_name: str,
    position: str,
    feedback_message: str,
    company_name: str = "Our Company"
) -> bool:
    """
    Send a feedback email with a custom message.
    """
    template_data = {
        "candidate_name": candidate_name,
        "company_name": company_name,
        "position": position,
        "custom_feedback": feedback_message
    }

    return send_email(
        id=f"feedback_{candidate_email}",
        email=candidate_email,
        status="feedback",
        template_data=template_data,
        sender_email=sender_email,
        sender_password=sender_password
    )


# success = send_invitation_email(
#     sender_email="hr@example.com",
#     sender_password="your-password",
#     candidate_email="john@example.com",
#     candidate_name="John Doe",
#     position="Software Engineer",
#     interview_date="2025-06-01",
#     interview_time="10:00 AM",
#     interview_location="Hyderabad Office"
# )
