# Template to deploy BBF bots in Streamlit Cloud Community

This repo can be used as a template to deploy any bot created with the
[BESSER-Bot-Framework](https://github.com/BESSER-PEARL/BESSER-Bot-Framework) in the [Streamlit Cloud](https://streamlit.io/cloud).

The bot must be created within a cached function (using the @st.cache_resource decorator)

- The function must always return the same value (e.g. True). This way the function (and the bot execution) is only run once.
- Always use the following bot platform: `websocket_platform = bot.use_websocket_platform(use_ui=False)  # IMPORTANT: USE_UI = FALSE`
- Run the bot without sleeping: `bot.run(sleep=False)  # IMPORTANT: SLEEP = FALSE`
- Call the `create_bot` function
- Then, run the streamlit_ui (the[default one](https://github.com/BESSER-PEARL/BESSER-Bot-Framework/blob/main/besser/bot/platforms/websocket/streamlit_ui.py)
  provided with BBF or your custom UI)
- Do not include `streamlit.host = localhost` and `streamlit.port = 5000` properties in the bot, they are ignored.