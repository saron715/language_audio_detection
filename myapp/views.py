from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings  # Assuming `MEDIA_ROOT` is configured
from gradio_client import Client , file
import requests
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User, auth
from .models import Profile
from django.http import JsonResponse
import base64
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from django.contrib import messages
import librosa
def home(request):
    return render(request, 'myapp/home.html')

def index(request):
    if not request.user.is_authenticated:
        return render(request, "myapp/login.html")
    return render(request, 'myapp/predict.html')

def predict_language(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        

        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        filename = fs.save(str(uuid.uuid4()), uploaded_file)  # Use a random string as the file name
        audio_file_path = fs.path(filename)
        mel_path = generate_mel_spectrogram(audio_file_path)


        try:
                # Prediction using gradio_client
            client = Client("saronium/Indian-language-identification-from-audio")
            language_result = client.predict(audio_file_path, api_name="/predict")
            
                # If the predicted language is Malayalam, convert the audio to text
            if language_result == 'malayalam':
                client = Client("saronium/kavyamanohar-Whisper-malayalam-trial")
                text_result = client.predict(audio_file_path, api_name="/predict")
                print(text_result)
                fs.delete(filename)
                return JsonResponse({'language': language_result, 'text': text_result, 'mel_path': mel_path})
            
            if language_result == 'tamil':
                client = Client("saronium/vasista22-whisper-tamil-medium")
                result = client.predict(param_0=file(audio_file_path),api_name="/predict")
                print(result)
                fs.delete(filename)
                return JsonResponse({'language': language_result, 'text': result, 'mel_path': mel_path})
            
            if language_result == 'hindi':
                client = Client("saronium/vasista22-whisper-hindi-small")
                result = client.predict(param_0=file(audio_file_path),api_name="/predict")
                fs.delete(filename)
                print(result) 
                return JsonResponse({'language': language_result, 'text': result, 'mel_path': mel_path})

            if language_result == 'english':
                 client = Client("saronium/jonatasgrosman-wav2vec2-large-xlsr-53-english")
                 result = client.predict(param_0=file(audio_file_path),api_name="/predict")
                 fs.delete(filename)
                 print(result) 
                 return JsonResponse({'language': language_result, 'text': result, 'mel_path': mel_path})
                    

            fs.delete(filename)
            return JsonResponse({'language': language_result,'mel_path': mel_path})

        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            return JsonResponse({'error': error_message}, status=500)

    
    return JsonResponse({'error': 'No audio file found'}, status=400)
     
            
from django.http import JsonResponse
from base64 import b64decode  # Import for base64 decoding



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import uuid
@csrf_exempt
def predict_response(request):
    if request.method == 'POST':
        audio = request.FILES['audio']

        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        filename = fs.save(str(uuid.uuid4()), audio)  # Use a random string as the file name
        audio_file_path = fs.path(filename)
        

        # Prediction using gradio_client
        try:
                # Prediction using gradio_client
                client = Client("saronium/Indian-language-identification-from-audio")
                language_result = client.predict(audio_file_path, api_name="/predict")
                
                # If the predicted language is Malayalam, convert the audio to text
                if language_result == 'malayalam':
                    client = Client("saronium/kavyamanohar-Whisper-malayalam-trial")
                    text_result = client.predict(audio_file_path, api_name="/predict")
                    print(text_result)
                    fs.delete(filename)
                    return JsonResponse({'language': language_result, 'text': text_result})
                if language_result == 'tamil':
                    client = Client("saronium/vasista22-whisper-tamil-medium")
                    result = client.predict(param_0=file(audio_file_path),api_name="/predict")
                    print(result)
                    fs.delete(filename)
                    return JsonResponse({'language': language_result, 'text': result})
            
                if language_result == 'hindi':
                    client = Client("saronium/vasista22-whisper-hindi-small")
                    result = client.predict(param_0=file(audio_file_path),api_name="/predict")
                    fs.delete(filename)
                    print(result) 
                    return JsonResponse({'language': language_result, 'text': result})

                if language_result == 'english':
                    client = Client("saronium/jonatasgrosman-wav2vec2-large-xlsr-53-english")
                    result = client.predict(param_0=file(audio_file_path),api_name="/predict")
                    fs.delete(filename)
                    print(result) 
                    return JsonResponse({'language': language_result, 'text': result})
                fs.delete(filename)
                return JsonResponse({'language': language_result})

        except Exception as e:
                error_message = f"An error occurred: {str(e)}"
                return JsonResponse({'error': error_message}, status=500)

    
    return JsonResponse({'error': 'No audio file found'}, status=400)

    

def login_view(request):
     if request.method == "POST":
        
        username = request.POST["username"]
        password = request.POST["password"]

        
        user = authenticate(request, username=username, password=password)

        
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
       
        else:
            return render(request, "myapp/login.html", {
                "message": "Invalid Credentials"
            })
        
       
    
     return render(request,"myapp/login.html")
    

def logout_view(request):
    logout(request)
    return render(request, "myapp/login.html", {
                "message": "Logged Out"
            })

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages

def signup(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(request, user)
            return redirect('index')  # Redirect to your desired page after signup
    else:
        user_form = UserCreationForm()

    context = {'user_form': user_form}
    return render(request, 'myapp/signup.html', context)


import uuid
import os
import numpy as np
import librosa
import librosa.display
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage


def generate_mel_spectrogram(audio_file_path):
    # Load the audio file
    y, sr = librosa.load(audio_file_path)
    
    # Generate the mel spectrogram
    mel_spec = librosa.feature.melspectrogram(y=y, sr=sr)
    mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
    
    # Plot and save the mel spectrogram as an image
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(mel_spec_db, sr=sr, x_axis='time', y_axis='mel')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel Spectrogram')
    media_folder = settings.MEDIA_ROOT

    subfolder = 'spectrograms'
    subfolder_path = os.path.join(media_folder, subfolder)
    os.makedirs(subfolder_path, exist_ok=True)  # Create the subfolder if it doesn't exist

    # Generate a filename for the spectrogram image
    filename = os.path.basename(audio_file_path)  # Use the original audio file name
    spectrogram_path = os.path.join(subfolder, filename + '.png')

    plt.savefig(os.path.join(settings.MEDIA_ROOT, spectrogram_path))
    plt.close()

    # Convert the file system path to a URL
    spectrogram_url = os.path.join(settings.MEDIA_URL, spectrogram_path).replace('\\', '/')
    print(spectrogram_url)
    # Return the URL to the saved mel spectrogram image
    return spectrogram_url

from django.http import HttpResponse
import numpy as np
from django.http import HttpResponse
from io import BytesIO
import tempfile
import subprocess

@csrf_exempt
def create_mel_spectrogram(request):
    if request.method == 'POST':
        audio = request.FILES['audio']
        current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"audio_{current_time}"  # Removed the .wav extension
        audio_path = os.path.join(settings.MEDIA_ROOT, filename)

        # Save the uploaded file to the media folder
        with open(audio_path, 'wb+') as destination:
            for chunk in audio.chunks():
                destination.write(chunk)

        # Convert the audio file to WAV format using FFmpeg
        wav_filename = f"{filename}.wav"
        wav_path = os.path.join(settings.MEDIA_ROOT, wav_filename)
        subprocess.run(["ffmpeg", "-i", audio_path, wav_path])

        # Now you can load the WAV file with librosa
        y, sr = librosa.load(wav_path)

        mel_spec = librosa.feature.melspectrogram(y=y, sr=sr)
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
        
        
        # Plot and save the mel spectrogram as an image
        plt.figure(figsize=(10, 4))
        librosa.display.specshow(mel_spec_db, sr=sr, x_axis='time', y_axis='mel')
        plt.colorbar(format='%+2.0f dB')
        plt.title('Mel Spectrogram')

        media_folder = settings.MEDIA_ROOT
        subfolder = 'spectrograms'
        subfolder_path = os.path.join(media_folder, subfolder)
        os.makedirs(subfolder_path, exist_ok=True)  # Create the subfolder if it doesn't exist

        # Generate a filename for the spectrogram image
        current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"spectrogram_{current_time}"
        spectrogram_path = os.path.join(subfolder, filename + '.png')

        plt.savefig(os.path.join(settings.MEDIA_ROOT, spectrogram_path))
        plt.close()

        # Convert the file system path to a URL
        spectrogram_url = os.path.join(settings.MEDIA_URL, spectrogram_path).replace('\\', '/')
        os.unlink(audio_path)
        os.unlink(wav_path)
        return HttpResponse(spectrogram_url, content_type="text/plain")
    else:
        return HttpResponse(status=400)
    
