from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.views.generic import UpdateView, DeleteView
from .models import *
from .forms import *
# Create your views here.
def login_page(request):
    forms = LoginForm()
    if request.method == 'POST':
        forms = LoginForm(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
    context = {'form': forms}
    return render(request, 'users/login.html', context)


def logout_page(request):
    logout(request)
    return redirect('login')

def book_list(request):
    book_list = BookEntry.objects.all()
    return render(request, 'catalog/book_list.html', {'book_list':book_list})

def member_list(request):
    memberlist = Member.objects.all()
    return render(request, 'catalog/member_list.html', {'memberlist': memberlist})

def book_issue_list(request):
    book_issue = BookIssue. objects.all()
    return render(request, 'catalog/book_issued_list.html', {'book_issue': book_issue})
        
def add_book(request):
    if not request.user.is_superuser:
        return redirect('login')
    form = BookAddForm()
    if request.method == 'POST':
        form = BookForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    context = {
        'form':form
    }
    return render(request, 'catalog/add_book.html', context=context)

def book_issue(request):
    if not request.user.is_superuser:
        return redirect('login')
    form = BookIssueForm()
    if request.method == 'POST':
        form = BookIssueForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_issue_list')
    context = {
        'form':form
    }
    return render(request, 'catalog/book_issue.html', context=context)

def add_member(request):
    if not request.user.is_superuser:
        return redirect('login')
    form = AddMemberForm()
    if request.method == 'POST':
        form = AddMemberForm(data = request.POST, files=request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            avatar = form.cleaned_data['avatar']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            retype_password = form.cleaned_data['retype_password']
            if password == retype_password:
                user = User.objects.create_user(username=username, password=password)
                print("--- after user.obj_create user---")
                user.member.first_name = first_name
                user.member.last_name = last_name
                user.member.email = email
                user.member.avatar = avatar
                print("--- before user.save---")
                user.save()
                print("--- after user.save---")
                # create_member = Member.objects.create(user=user, first_name=first_name, last_name=last_name, email=email, avatar=avatar)
                # create_member = form.save(commit=False)
                # create_member.save()
                return redirect('member_list')
            return redirect('member_list')
    context = {
        'form':form
    }
    return render(request, 'catalog/add_member.html', context=context)

'''
class BookListUpdateView(UpdateView):
    form = BookAddForm
    model = BookEntry
    fields = '__all__'
    template_name = 'catalog/book_edit.html'
    success_url = reverse_lazy('book_list')

    def form_valid(self, form):
        bookedit = BookEntry.objects.get(user=self.request.user)
        if form.instance.author == bookedit:
            return super().form_valid(form)

        else:
            form.add_error(None, "You need to be the author in order to update the post")
            return super().form_valid(form)
'''
def edit_book(request, pk):
    if not request.user.is_superuser:
        return redirect('login')
    book_instance = BookEntry.objects.get(isbn=pk)
    form = BookAddForm(instance= book_instance)
    if request.method == 'POST':
        form = BookForm(data=request.POST, files=request.FILES, instance=book_instance)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    context = {
        'form':form
    }
    return render(request, 'catalog/book_edit.html', context=context)

def book_issue_edit(request, pk):
    if not request.user.is_superuser:
        return redirect('login')
    book_instance = BookIssue.objects.get(id=pk)
    form = BookIssueForm(instance=book_instance)
    if request.method == 'POST':
        form = BookIssueForm(data = request.POST, files = request.FILES, instance=book_instance)
        if form.is_valid():
            form.save()
            return redirect('book_issue_list')
    context = {
        'form':form
    }
    return render(request, 'catalog/book_issue_edit.html', context=context)
