import markdown as md
import random
import math
from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request,title):
    if util.get_entry(title):
        content=util.get_entry(title)
        return render(request,"encyclopedia/content.html",{
            "title": title.upper(),
            "content":md.markdown(content)
        })
    else:
        return render(request,"encyclopedia/error.html")

def search(request):
    query=request.POST.get("q")
    new=[]
    if util.get_entry(query):
        return redirect('title',title=query)
    else:
        all_entries=util.list_entries()
        for l in all_entries:
            s1=str(query).lower()
            s2=str(l).lower()
            if(s2.find(s1)!=-1):
                new.append(l)
        if len(new)==0:
            return render(request,"encyclopedia/error.html")
        else:
            return render(request, "encyclopedia/searchpage.html", {
        "entries": new
    })

def create(request):
    return render(request,"encyclopedia/create.html")

def save(request):
    title = request.POST.get("title")
    text = request.POST.get("markdown")
    if util.get_entry(title):
        return render(request,"encyclopedia/pageexists.html",{
            "entry":title
        })
    else:
        util.save_entry(title,text)
        return redirect('title',title=title)


def editpage(request,title):
    return render(request,"encyclopedia/editpage.html",{
        "title":title.capitalize(),
        "content":util.get_entry(title)
    })

def edit(request,title):
    content=request.POST.get("markdown")
    ti=title.capitalize()
    util.save_entry(ti,content)
    return redirect('title',title=ti)

def randompage(request):
    all_entries=util.list_entries()
    l=len(all_entries)
    i=random.randint(0,l-1)
    return redirect('title',title=all_entries[i])
