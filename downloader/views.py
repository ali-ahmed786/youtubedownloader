from django.shortcuts import render
import pytube
from django.shortcuts import redirect
from pytube import YouTube 
from django import forms
from django.http import FileResponse
from django.http import HttpResponse
import requests
from urllib.request import Request, urlopen    
import os
import re
from moviepy.editor import *

from django.core.mail import send_mail
import unicodedata
import re

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')
from_email= "lexdoyle2@gmail.com"

class downloadInput(forms.Form):
     urlInput= forms.CharField(label="Video URL ")

def index(request):
     return render(request, "downloader/index.html", {
        "formremove": downloadInput()
        
     })
def download(request):
     try:
          global url
          url = request.POST.get('urlinput')
          stream= pytube.YouTube(url).streams.all()
          global title
          title =YouTube(url).title
          print(title)          
          resolutions=[]
          global directory
          directory = "../youtubedownloader/downloader/static/downloader"
          files_in_directory = os.listdir(directory)
          filtered_files = [file for file in files_in_directory if file.endswith(".mp4")]
          for file in filtered_files:
           path_to_file = os.path.join(directory, file)
           os.remove(path_to_file)
          filtered_filesmp3 = [file for file in files_in_directory if file.endswith(".mp3")]
          for file in filtered_filesmp3:
               path_to_file = os.path.join(directory, file)
               os.remove(path_to_file)
          for i in stream:
               resolutions.append(i.resolution)
               resolutions= list(dict.fromkeys(resolutions))
          if "watch?v=" in url:
               global embed 
               embed = url.replace("watch?v=", "embed/")
          else:
               
               key= url.split("https://youtu.be/", 1)[1]
               embed="https://www.youtube.com/embed/" + key
               print(embed)
          return render(request, "downloader/download.html", {
                    "url" : embed, 
                    "stream": stream,
                    "resolutions": resolutions
               })
     except:
          alert = "👮🐧Please enter a Valid URL‼️"
          return render(request, "downloader/index.html", {
               "message" : alert})

def download2(request):
     try:
          newtitle=slugify(title)
          YouTube(url).streams.filter(only_audio=True).first().download("../youtubedownloader/downloader/static/downloader", skip_existing=True, filename= newtitle)
          mp4_file=newtitle+ ".mp4"
          mp3_file=newtitle+ ".mp3"
          serverstoragedir = "../youtubedownloader/downloader/static/downloader"
          vidpath = os.path.join(serverstoragedir, mp4_file)
          audpath = os.path.join(serverstoragedir, mp3_file)
          #YouTube(url).streams.filter(only_audio=True).first().download("..\youtubedownloader\downloader\static\downloader",skip_existing=True, filename="audio", )
          #mp4_file="audio"+ ".mp4"
          #mp3_file="audio"+ ".mp3"
          #newdirectory =directory + r'\static\downloader'
          #vidpath = os.path.join(newdirectory, mp4_file)
          #audpath = os.path.join(newdirectory, mp3_file)
          audioclip = AudioFileClip(vidpath)
          audioclip.write_audiofile(audpath, verbose=False)
          audioclip.close()
          audpath="downloader/"+newtitle+".mp3"
          return render(request, "downloader/final_Step.html", {
                    "audpath" : audpath})
     except:
          return render(request, "downloader/index.html", {
               "message": "Please start again 😄😄"
          })

def download3(request):
     try:
          video_res= request.POST.get('selected_res')
          newtitle=slugify(title)
          YouTube(url).streams.filter(res=video_res).first().download("../youtubedownloader/downloader/static/downloader",skip_existing=True, filename= newtitle)
          vidpath="downloader/"+newtitle+".mp4"
          return render(request, "downloader/final_Step.html", {
                    "audpath" : vidpath})
     except:
          return render(request, "downloader/index.html", {
               "message": "Please start again 😄😄"
          })


def suggestions(request):
     return render(request, "downloader/suggestions.html")
def features(request):
     return render(request, "downloader/features.html")
def suggestionform(request):
     name =request.POST.get('name')
     email = request.POST.get('email')
     suggestion= request.POST.get('suggestion')
     subject="Youtube Downloader Suggestion form submission"
     message = "_________________________Form submission record___________________________"+ "\n"+"Sender name: " + name +"\n" + "Sender's email: " + email +"\n" +  "Suggestion: "+ suggestion
     directory = os.getcwd()
     newpath= os.path.join(directory, "suggestions.txt")
     print(newpath)

     if message!="":
          try:
               formfile= open(newpath,'a')
               print(message)
               formfile.write(message + '\n')
               formfile.close()
               alert = "🥳🐯🥳Your suggestions have been submitted. THANK YOU"
               return render(request, "downloader/index.html", {
               "message": alert})
          except:
               alert = "There was an error during submission 😣🦊😣"
               return render(request, "downloader/index.html", {
               "message": alert})
