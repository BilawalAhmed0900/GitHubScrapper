import requests
from django.shortcuts import render
from django.http import HttpResponse
import urllib.parse
from bs4 import BeautifulSoup


# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, 'base.html')


def search_view(request, *args, **kwargs):
    tag = request.POST.get("tag")
    page_num = request.POST.get("page")
    if tag is None:
        return render(request, 'base.html')

    if page_num is None:
        page_num = 1
    else:
        page_num = int(page_num)

    tag = str(tag)
    tag_orig = tag
    tag = urllib.parse.quote_plus(tag)
    github_search_url = f"https://github.com/search?p={page_num}&q={tag}&type=users"
    page = requests.get(github_search_url)
    if page.status_code != 200:
        return render(request, 'error.html')

    bs = BeautifulSoup(page.content, "html.parser")
    user_results_div = bs.find("div", {"id": "user_search_results"})
    if user_results_div is None:
        return render(request, 'error.html')

    under_div = user_results_div.find("div", {"class": "Box border-0"})
    users_list_div = under_div.find_all("a", {"class": "mr-1"})

    users_list = []
    for index, child in enumerate(users_list_div):
        full_name = child.text.strip()
        user_name = child.find_next("a").text.strip()
        note = child.find_next("p", {"class": "mb-1"})
        if note is not None:
            note = note.text.strip().replace("\r", "").replace("\n", "")
        else:
            note = ""
        users_list.append([index + 1, full_name, user_name, note])

    context = {
        "page": page,
        "tag": tag,
        "users": users_list,
        "requests_upper": {
            "tag": tag_orig,
            "page": page_num
        }
    }
    return render(request, 'search.html', context=context)
