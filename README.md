<h1>Mini-On Chatbot</h1>
<p>Powered by Gemini Flash</p>
<h3>Pre-Requisites</h3>  
1.  API token for Gemini AI<br>
2.  API token for OpenWeather<br>
<h3>Workflow</h3>
1.  In command line, reach the working directory of manage.py<br>
2.  Run `py manage.py runserver`<br>
3.  You will see auth.html running in localhost<br>
4.  Enter the API tokens appropriately in the form<br>
5.  After authenticating, You will see the window with our chatbot.<br>
6.  Prompts about weather might not work until the word 'weather' appears in the prompt and location field is filled.<br>
7.  Choose one of the provided tones.<br>
8.  Chat with the bot just like any other bot, in an interface designed to be intuitive and easy to use.<br>
<h3>How does it work</h3>
1.  Uses GeminiAI API call for each prompt.<br>
2.  Each prompt is engineered, to make it seem like the Chatbot has memory.<br>
3.  A memory buffer of 5 prompts is added to each prompt.<br>
4.  Weather details from API call fetched if location is not none and added to the prompt as well.<br>
5.  Thus the engineered prompt looks like this <br>
    f"You are a helpful assistant. Only mention weather if the user asks about it. "<br>
    f"Don't bring up weather on your own. Respond in a {tone} tone. "<br>
    f"Past prompts:\n{chr(10).join(prompt_buffer)}\n"<br>
    f"Weather: {weather_info if weather_info else 'N/A'}\n"<br>
    f"User: {user_prompt}"<br>
<h3>Output Screenshots</h3>
<img src=''>
<img src=''>
