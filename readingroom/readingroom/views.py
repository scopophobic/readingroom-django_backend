from django.shortcuts import render



def home(request):
    context = {
        "user": request.user  # Django automatically attaches the user
    }
    return render(request, 'home.html',context)