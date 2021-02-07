from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from backend.models import *
@login_required(login_url='login')
def dashboard(request):
    total_book = BookEntry.objects.count()
    total_member = Member.objects.count()
    total_book_issue = BookIssue.objects.count()
    total_book_return = BookReturn.objects.count()
    context = {
        'total_book': total_book,    
        'total_member': total_member,
        'total_book_issue': total_book_issue,
        'total_book_return': total_book_return,
    }
    return render(request, 'dashboard.html', context=context)

def book_list(request):
    book_list = BookEntry.objects.all()
    return render(request, 'dashboard.html', {'book_list':book_list})
'''
from django.http import HttpResponse
from django.shortcuts import render

def HomeView(request):
    user = request.user
    hello = "Hello World"

    context = {
        'user' : user,
        'hello': hello
    }

    return render(request, 'main/home.html', context=context)
'''