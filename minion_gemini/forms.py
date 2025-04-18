from django import forms
class PromptForm(forms.Form):
    prompt = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Type your message...',
            'autocomplete': 'off'
        })
    )

class TokenForm(forms.Form):
    gemini_token = forms.CharField(required=True)
    open_weather_token = forms.CharField(required=True)