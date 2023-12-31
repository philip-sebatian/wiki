from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
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
    
    title=forms.CharField(widget=forms.Textarea(attrs={"class":"titlef"}))
    content=forms.CharField(widget=forms.Textarea(attrs={"class":"contentf"}))

class entryform2(forms.Form):
    
    title=forms.CharField(widget=forms.Textarea(attrs={"class":"titlef",'readonly':'readonly'}))
    content=forms.CharField(widget=forms.Textarea(attrs={"class":"contentf"}))

def convert(file):
    f=open(file,"r")
    x=f.read()
    x=markdown2.markdown(x)
    return x

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request):
    if request.method=='POST':
        f=entryform(request.POST)
        if f.is_valid():
            data=f
            data=data.cleaned_data
            x=data["content"]
            with open("entries/"+data['title']+".md",'w+') as a:
                a.write(x)
            return render(request,"encyclopedia/wiki.html",{
            "entries":util.list_entries()
            })
    return render(request,"encyclopedia/wiki.html",{
        "entries": util.list_entries()

    })


def read(request,name):
    if request.method=="POST":
        data=request.POST
        title=data.get('title')
        x=data.get("content")
        with open("entries/"+data['title']+".md",'w+') as a:
            a.write(x)
        html=convert("entries/"+title+".md")
        return render(request,"encyclopedia/read.html",{
            "html":html,'name':title,'markup':x
        })

    
    html="entries/"+str(name)+".md"
    try:
        with open(html,'r') as f:
            markup=f.read()
    except:
        return render(request,"encyclopedia/error.html",{
        "html":"ERROR ENTRY NOT FOUND","name":name,
        
    })



    html=convert(html)
    
        
    
    return render(request,"encyclopedia/read.html",{
        "html":html,"name":name,'markup':markup
        
    })

def add(request):
    curr_entries=util.list_entries()
    if request.method=="POST":
        data=entryform(request.POST)
        
        if data.is_valid():
            
            data=data.cleaned_data
            title=data["title"]
            if title in listofmds():
                return render(request,"encyclopedia/error.html",{
            "html":"ENTRY ALREASY EXISTS"
        })
                
            if title not in listofmds():
                content=str(data['content'])
                f=open("entries/"+str(title)+".md","w+")
                f.write(content)
                f.close()
                
                x=convert("entries/"+title+".md")
                
                
                return render(request,"encyclopedia/wiki.html",{
                "html":x,"name":title,'markup':content
            })
    return render(request,"encyclopedia/add.html",{
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

def search(request):
    similar=[]
    if request.method=="POST":
        s_info=request.POST
        
        
        searchdata=s_info["q"]
        result=util.get_entry(searchdata)
        if result:
            result=markdown2.markdown(result)
        if result:
            return render(request,"encyclopedia/search.html",{
            "html":result
        })

        for i in util.list_entries():
            if searchdata.lower() in i.lower() :
                similar.append(i)

        if len(similar)!=0:
            return render(request,"encyclopedia/searchsim.html",{
            "html":similar
        })
        return render(request,"encyclopedia/search.html",{
                "html":"NO SIMILAR ENTRIES"
            })
    
def edit(request):
        
    
    data=request.POST
   
    title=data.get('title')
    content=data.get("content")

    return render(request,"encyclopedia/edit.html",{
                'form':entryform2({"title":str(title),'content':str(content)}),"titlemd":title,'name':title
        })
    
