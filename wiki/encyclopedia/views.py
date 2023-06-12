from django.shortcuts import render

from . import util

from random import choice


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def search(request):
    if request.method == "POST":
        word = (request.POST)['q']
        txt = util.get_entry(word)
        if txt is not None:
            return render(request, "encyclopedia/title.html", {
                "title": word,
                "body": util.convert(txt)
            })
        else:
            substr = util.entry_substr(word)
            if len(substr) < 1:
                empty = f"Your search -{word}- nid not match any document"
                return render(request, "encyclopedia/error.html", {
                    "title": f"Search Results for {word}",
                    "body": empty
                })

            else:
                result = (substr)
                return render(request, "encyclopedia/search.html", {
                    "keyword": word,
                    "text": result
                })


def new(request):
    if request.method == "POST":
        title = (request.POST)['title']
        content = (request.POST)['content']
        if not title or not content:
            return render(request, "encyclopedia/error.html", {
                "title": "Invalid Entry",
                "body": ('<h1 style="margin-top: 250px; text-align: center; font-size: 500%;"> <b>Invalid Entry </b></h1>')
            })
        else:
            exist = util.check(title)
            if exist == 1:
                return render(request, "encyclopedia/error.html", {
                    "title": "Already Exists",
                    "body": ('<h1 style="margin-top: 250px; text-align: center; font-size: 500%;"> <b>404: The entry already exists</b></h1>')
                })
            else:
                try:
                    util.save_entry(title, content)
                    txt = util.get_entry(title)
                    return render(request, "encyclopedia/title.html", {
                        "title": title,
                        "body": util.convert(txt)
                    })
                except:
                    return render(request, "encyclopedia/error.html", {
                        "title": "503 Service Unavailable",
                        "body": ('<h1 style="margin-top: 250px; text-align: center; font-size: 500%;"> <b>404: 503 Service Unavailable:Error has occurred </b></h1>')
                    })
    else:
        return render(request, "encyclopedia/new_page.html")

def edit(request):
    if request.method == "POST":
        title = (request.POST)['title']
        txt = util.get_entry(title)
        if txt is not None:
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "body": txt
            })
        else:
            return render(request, "encyclopedia/error.html", {
                        "title": "503 Service Unavailable",
                        "body": ('<h1 style="margin-top: 250px; text-align: center; font-size: 500%;"> <b>404: 503 Service Unavailable:Error has occurred </b></h1>')
                    })


def re_new(request):
    if request.method == "POST":
        title = (request.POST)['title']
        content = (request.POST)['content']
        if not title or not content:
            return render(request, "encyclopedia/error.html", {
                "title": "Invalid Entry",
                "body": ('<h1 style="margin-top: 250px; text-align: center; font-size: 500%;"> <b>Invalid Entry </b></h1>')
            })
        else:
                try:
                    util.save_entry(title, content)
                    txt = util.get_entry(title)
                    return render(request, "encyclopedia/title.html", {
                        "title": title,
                        "body": util.convert(txt)
                    })
                except:
                    return render(request, "encyclopedia/error.html", {
                        "title": "503 Service Unavailable",
                        "body": ('<h1 style="margin-top: 250px; text-align: center; font-size: 500%;"> <b>404: 503 Service Unavailable:Error has occurred </b></h1>')
                    })
    return render(request, "encyclopedia/error.html", {
                        "title": "503 Service Unavailable",
                        "body": ('<h1 style="margin-top: 250px; text-align: center; font-size: 500%;"> <b>404: 503 Service Unavailable:Error has occurred </b></h1>')
                    })


def random_page(request):
    list = util.list_entries()
    title = choice(list)
    txt = util.get_entry(title)
    return render(request, "encyclopedia/title.html", {
            "title": title,
            "body": util.convert(txt)
        })


def title(request, word):
    txt = util.get_entry(word)
    if txt is None:
        return render(request, "encyclopedia/error.html", {
            "title": "404 page not found",
            "body": ('<h1 style="margin-top: 250px; text-align: center; font-size: 500%;"> <b>404: page not found</b></h1>')
        })
    else:
        return render(request, "encyclopedia/title.html", {
            "title": word,
            "body": util.convert(txt)
        })
