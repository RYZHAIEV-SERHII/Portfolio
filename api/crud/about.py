from api.schemas.about import AboutInfoResponse, AboutInterestsResponse

from logging_setup import api_logger


async def get_about_info() -> AboutInfoResponse:
    """
    Retrieve the about me information.

    Returns:
        AboutInfoResponse: The about me information.
    """
    about_info = """
    👋 Hello!
    I’m Serhii, aspiring Junior Python Developer with a solid foundation in web development through a
    comprehensive Python Developer course and self-paced study. Passionate about learning new
    technologies and improving coding skills. Experienced in building various pet projects, including a
    Telegram bot and a blog platform.

    🚀 My Mission
    I’m eager to explore new technologies and best practices. I thrive on solving complex problems and
    turning ideas into reality. My goal is to stay at the forefront of the tech landscape, continuously
    improving and expanding my expertise.

    📫 Let’s Connect!
    I’m always open to collaborations and exciting projects. Whether you’re a fellow developer or a tech
    enthusiast, I’m eager to connect and build something amazing together. Let’s turn ideas into reality!
    Happy coding! 🖥️
"""
    api_logger.info("About me info. Status: retrieved")
    return AboutInfoResponse(info=about_info)


async def get_all_interests() -> AboutInterestsResponse:
    """
    Retrieve the list of interests.

    Returns:
        AboutInterestsResponse: The list of interests.
    """
    api_logger.info("Interests. Status: retrieved")
    return AboutInterestsResponse(
        interests=[
            "Python",
            "Web Development",
            "API Development",
            "Automation",
            "Artificial Intelligence",
            "E-Commerce Development",
            "Natural Language Processing (NLP)",
            "Bot Development",
            "Freelancing and Consulting",
        ]
    )
