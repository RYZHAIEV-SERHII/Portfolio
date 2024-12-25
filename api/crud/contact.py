from api.schemas.contact import ContactInfoResponse, SocialProfile
from logging_setup import api_logger


async def get_contact_info():
    """
    Retrieve the contact information.

    Returns:
        ContactInfoResponse: The contact information.
    """
    api_logger.info("Contact info. Status: retrieved")
    return ContactInfoResponse(
        address="Ukraine, Vinnytsia",
        social_profiles=[
            SocialProfile(
                name="LinkedIn", url="https://www.linkedin.com/in/serhii-ryzhaiev"
            ),
            SocialProfile(name="GitHub", url="https://github.com/RYZHAIEV-SERHII"),
            SocialProfile(name="GitLab", url="https://gitlab.com/RYZHAIEV-SERHII"),
            SocialProfile(name="Telegram", url="https://t.me/CTAJIKEP"),
        ],
        email="serhii.ryzhaiev@gmail.com",
        phone="+38 (097) 806 87 46",
        notification="If you have any questions, please visit my '/contact' page "
        "on my portfolio site and leave a message in a 'Contact Me' form. "
        "We can discuss it further.",
    )
