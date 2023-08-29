from django.shortcuts import render
from django import forms

from . import util
import markdown2
import os 
import random
entries=util.list_entries()
def listofmds():
    path="entries"
    listofmd=os.listdir(path)
    for i in range(len(listofmd)):
        x=listofmd[i].split(".")
        listofmd[i]=x[0]
    return listofmd



class entryform(forms.Form):
    
    title=forms.CharField(widget=forms.TextInput(attrs={"class":"titlef"}))
    content=forms.CharField(widget=forms.TextInput(attrs={"class":"contentf"}))

def convert(file):
    f=open(file,"r")
    x=f.read()
    x=markdown2.markdown(x)
    return x

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

def wiki(request):
    return render(request,"encyclopedia/wiki.html",{
        "entries": entries

    })

def read(request,name):
    
    html="entries/"+str(name)+".md"
    html=convert(html)
    
        
    
    return render(request,"encyclopedia/read.html",{
        "html":html
        
    })

def add(request):
    if request.method=="POST":
        data=entryform(request.POST)
        
        if data.is_valid():
            
            data=data.cleaned_data
            title=data["title"]
            if title in listofmds():
                return render(request,"encyclopedia/edit.html",{
            "form":entryform()
        })
                
            content=str(data['content'])
            f=open("entries/"+str(title)+".md","w+")
            f.write(content)
            f.close
            return render(request,"encyclopedia/edit.html",{
                "form":entryform()
            })
    return render(request,"encyclopedia/edit.html",{
            "form":entryform()
        })

        

def randoms(request):
    x=random.randint(0,len(entries)-1)
    entry=entries[x]
    path="entries/"+entry+".md"
    html=convert(path)
    return render(request,"encyclopedia/read.html",{
        "html":html
    })
    