from random import randint
import re
import markdown2

from django.shortcuts import render, redirect
from django.http import *
from django.contrib import messages
from django.urls import reverse

from . import forms
from . import util


#Complete     
def index(request):
    """
    This function handels entire index_page/Home_page
    """

    if request.method == "GET":
        titles = util.list_entries()
        return render(request, "encyclopedia/index.html", {
                        "entries": titles
                        })
    else:
        return HttpResponseBadRequest("Not GET request made")

#Complete
def entryPage(request, title, flag=None):

    """
    Handles entry page
    Returns content of single entry by using title as parameter
    also Returns "No such entry present" message if entry with the given title is not present
    """

    title = title
    entry = util.get_entry(title)
    if entry is not None:        
        return render(request, "encyclopedia/entry.html", {
            "entry":markdown2.markdown(entry) ,
            "title": title,
            "flag": flag ,
         })

    else:
        response = render(request, "encyclopedia/notfound.html",)
        response.status_code = 404
        return response
            
#Complete
def createPage(request):

    """
    This view handles creation of new entries
    """

    if request.method == "POST":
        form = forms.createPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']

            if util.get_entry(title) is not None:
                messages.error(request, "This entry already exist")
                return HttpResponseRedirect(reverse("entryPage", args=(title,)))
            else:
                content = form.cleaned_data["content"]
                util.save_entry(title, content)
                messages.add_message(request, messages.SUCCESS, "Your entry has been saved succesfully")
                return HttpResponseRedirect(reverse("entryPage", args=(title,)))

        else:
            
            return render(request, "encyclopedia/create_page.html", {
            "form": forms.createPage(),
            })

    else:        
        return render(request, "encyclopedia/create_page.html", {
        "form": forms.createPage(),
        })

#Complete
def updateEntry(request):
    """
    This function updates entry
    """
    if request.method == "POST":
        form = forms.createPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            messages.success(request, "Your entry has UPDATED succesfully")
            return HttpResponseRedirect(reverse("entryPage", args=(title,)))
    else:
        messages.error(request, "Some error occured")
        return HttpResponseRedirect('createPage')

#Complete
def RandomPage(request):

    """
    This view Displays random Entry """

    entries = util.list_entries()
    random_entry = randint(0, (len(entries)-1))

    return entryPage(request, entries[random_entry])

#Complete
def editPage(request):
    """
    This view edit the entry and saves it """

    if request.method == "POST":
        rcvTitle = forms.edit(request.POST)

        if rcvTitle.is_valid():
            title = rcvTitle.cleaned_data["rcvTitle"]
            populated = forms.createPage(initial = {"content": util.get_entry(title)})
            return render(request, "encyclopedia/edit.html", {"form": populated, "title": title})
        
        else:
            messages.error(request, "Invalid data: Re-update the entry")
            return render(request, "encyclopedia/Edit.html", {"form": populated, "title": title})

#Complete
def search(request):

    """
    Handels search query
    and returns HttpResponse of entry page of query made
    """

    if request.method == "GET":
        search = forms.search(request.GET)
        if search.is_valid():
            query = search.cleaned_data['q']
            entryList = util.list_entries()

            matched = set() #list of matched entries
            for entry in entryList:
                obj = re.search(r'{query}'.format(query = query), entry) #! Not matching exact query
                if obj is not None:
                    matched.add(entry)

            if len(matched) == 0:
                messages.info(request, "No match found")
                return render(request,'encyclopedia/search.html', {"results": entryList})

            elif (len(matched) == 1) and ( query in matched):
                return HttpResponseRedirect(reverse('entryPage', args=(query,)))
                
            else:
                return render(request, "encyclopedia/search.html", { "results": matched }) 
    
    else:
        return redirect("index")

           