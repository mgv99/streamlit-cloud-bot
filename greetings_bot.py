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

# This script is run on every interaction with the UI with every user. A Streamlit session is created for each
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
    # Add here intents, states, bodies...
    # Load bot properties stored in a dedicated file
    bot.load_properties('config.ini')
    # Define the platform your chatbot will use
    websocket_platform = bot.use_websocket_platform(use_ui=False) # IMPORTANT: USE_UI = FALSE

    # STATES

    initial_state = bot.new_state('initial_state', initial=True)
    hello_state = bot.new_state('hello_state')
    good_state = bot.new_state('good_state')
    bad_state = bot.new_state('bad_state')

    # INTENTS

    hello_intent = bot.new_intent('hello_intent', [
        'hello',
        'hi',
    ])

    good_intent = bot.new_intent('good_intent', [
        'good',
        'fine',
    ])

    bad_intent = bot.new_intent('bad_intent', [
        'bad',
        'awful',
    ])

    # STATES BODIES' DEFINITION + TRANSITIONS

    initial_state.when_intent_matched_go_to(hello_intent, hello_state)

    def hello_body(session: Session):
        websocket_platform.reply(session, 'Hi! How are you?')
        websocket_platform.reply_options(session, ['Good', 'Bad'])

    hello_state.set_body(hello_body)
    hello_state.when_intent_matched_go_to(good_intent, good_state)
    hello_state.when_intent_matched_go_to(bad_intent, bad_state)

    def good_body(session: Session):
        session.reply('I am glad to hear that!')

    good_state.set_body(good_body)
    good_state.go_to(initial_state)

    def bad_body(session: Session):
        session.reply('I am sorry to hear that...')

    bad_state.set_body(bad_body)
    bad_state.go_to(initial_state)

    print('running the bot')
    bot.run(sleep=False)  # IMPORTANT: SLEEP = FALSE
    # Always return true
    return True


# Create the bot (only once thanks to the caching mechanism)
create_bot()
# Use the default streamlit_ui in BBF, or feel free to copy-paste its code in a new file in your repo and modify it as
# you want. For instance, removing the 'file uploading' component in the ui.
# The ui code is a mess, so good luck if you want to move around it :)
streamlit_ui.main()
