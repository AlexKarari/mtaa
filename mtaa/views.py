from django.shortcuts import render
from .models import Profile, Hood, Business, Post, save_user_profile
# Create your views here.
def index(request):
    return render(request, 'all/index.html')


def search_results(request):

    if 'business' in request.GET and request.GET["business"]:
        search_term = request.GET.get("business")
        searched_businesses = Business.search_by_bizName(search_term)
        message = f"{search_term}"

        return render(request, 'all/search.html', {"message": message, "searched_businesses": searched_businesses})

    else:
        message = "You haven't searched for any term"
        return render(request, 'all/search.html', {"message": message})
