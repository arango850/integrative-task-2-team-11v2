from django.shortcuts import render

# Create your views here.
# chatbot/views.py



def chatbot_view(request):
    return render(request, 'chatbot.html')

