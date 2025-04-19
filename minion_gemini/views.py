import os
import requests
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from dotenv import load_dotenv
from google import genai
from .forms import PromptForm, TokenForm
from .models import Conversation


GEMINI_API_KEY=''
WEATHER_API_KEY=''

# In-memory buffer
prompt_buffer = []
MAX_BUFFER = 5

global genai_client

def auth(request):
    tf=TokenForm()
    if request.method=='POST':
        tf=TokenForm(request.POST)
        if tf.is_valid():
            gemini_token=tf.cleaned_data['gemini_token']
            open_weather_token=tf.cleaned_data['open_weather_token']
            global GEMINI_API_KEY 
            GEMINI_API_KEY = gemini_token
            global WEATHER_API_KEY 
            global genai_client
            WEATHER_API_KEY = open_weather_token
            genai_client=genai.Client(api_key=GEMINI_API_KEY)
            if genai_client:
                return redirect(home)
    return render(request,'auth.html',{'form':tf})

@csrf_exempt
def home(request):
    form = PromptForm()
    if request.method == 'POST':
        form = PromptForm(request.POST)
        if form.is_valid():
            print(GEMINI_API_KEY)
            user_prompt = form.cleaned_data['prompt']
            tone = form.cleaned_data.get('tone','casual')
            location = form.cleaned_data.get('location','chennai')

            weather_info = get_weather(location) if "weather" in user_prompt.lower() else ''

            if len(prompt_buffer) >= MAX_BUFFER:
                prompt_buffer.pop(0)
            prompt_buffer.append(user_prompt)

            full_prompt = (
                f"You are a helpful assistant. Only mention weather if the user asks about it. "
                f"Don't bring up weather on your own. Respond in a {tone} tone. "
                f"Past prompts:\n{chr(10).join(prompt_buffer)}\n"
                f"Weather: {weather_info if weather_info else 'N/A'}\n"
                f"User: {user_prompt}"
            )

            gemini_response = query_gemini(full_prompt)
            Conversation.objects.create(user_prompt=user_prompt, response=gemini_response)

            return JsonResponse({'response': gemini_response})

    conversations = Conversation.objects.all()
    return render(request, 'index.html', {'form': form, 'conversations': conversations})


def query_gemini(prompt):
    try:
        response = genai_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text
    except:
        return "Error: Failed to generate response."

def get_weather(location):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        return f"{data['weather'][0]['description']} at {data['main']['temp']}°C"
    except:
        return "Weather info unavailable."
