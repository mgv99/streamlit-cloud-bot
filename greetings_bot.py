# You may need to add your working directory to the Python path. To do so, uncomment the following lines of code
# import sys
# sys.path.append("/Path/to/directory/bot-framework") # Replace with your directory path

import logging
import streamlit as st
from besser.bot.core.bot import Bot
from besser.bot.core.session import Session
from besser.bot.platforms.websocket import streamlit_ui

# Configure the logging module
logging.basicConfig(level=logging.INFO, format='{levelname} - {asctime}: {message}', style='{')

# This script is re-run on every interaction with the UI with every user. A Streamlit session is created for each
# connected user (creating also its bot session).
# We only want to create the bot once, so we must create it within a function tagged with the @st.cache_resource
# decorator.

# Add streamlit style configuration properties here (not necessary)
# More info: https://docs.streamlit.io/library/api-reference/utilities/st.set_page_config
st.set_page_config(
    page_title="Streamlit Chat - Demo",
)


# This function is cached, so it will be run only when its output changes.
# We return always true, so it will be run only once (when the 1st user connects)
# More info here: https://docs.streamlit.io/library/advanced-features/caching
@st.cache_resource
def create_bot():
    # Create here your bot
    # End the function with the following:
    # Create the bot
    bot = Bot('greetings_bot')
    # Load bot properties stored in a dedicated file
    bot.load_properties('config.ini')
    # Define the platform your chatbot will use
    websocket_platform = bot.use_websocket_platform(use_ui=False)  # IMPORTANT: USE_UI = FALSE
    # Add here intents, states, bodies...
    bot.run(sleep=False)  # IMPORTANT: SLEEP = FALSE
    # Always return true
    return True


# Create the bot (only once thanks to the caching mechanism)
create_bot()
# Use the default streamlit_ui in BBF, or feel free to copy-paste its code in a new file in your repo and modify it as
# you want. For instance, removing the 'file uploading' component in the ui.
# The ui code is a mess, so good luck if you want to move around it :)
streamlit_ui.main()
