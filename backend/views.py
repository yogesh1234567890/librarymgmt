from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db import transaction
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.forms import widgets
from django.forms import inlineformset_factory
from .models import *
from .forms import *
from django.contrib.auth.models import User


#----------------------------------------- login and logour views --------------------------------------
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


# ----------------------------- Book CRUD views ------------------------------------------
def book_list(request):
    book_list = BookEntry.objects.all().order_by('-isbn')
    return render(request, 'catalog/book_list.html', {'book_list': book_list})
    
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

def view_book(request, pk):
    if not request.user.is_superuser:
        return redirect('login')
    book_instance = BookEntry.objects.get(isbn=pk)
    form = BookAddForm(instance= book_instance)
    context = {
        'form':form
    }
    return render(request, 'catalog/book_detail.html', context=context)

class BookDeleteView(DeleteView):
    model = BookEntry
    template_name = 'catalog/confirm_delete.html'
    success_url = reverse_lazy('book_list')


# ----------------------------- Library member CRUD views ------------------------------------------
def member_list(request):
    memberlist = Member.objects.all()
    return render(request, 'catalog/member_list.html', {'memberlist': memberlist})

def add_member(request):
    if not request.user.is_superuser:
        return redirect('login')
    form = AddMemberForm()
    if request.method == 'POST':
        form = AddMemberForm(request.POST, request.FILES)
        if form.is_valid():   
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            avatar = form.cleaned_data['avatar']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            retype_password = form.cleaned_data['retype_password']
            if password == retype_password:
                print("---------1----------------")
                member_user = User.objects.create_user(username=username, password=password)
                print(member_user,"-----I am user----------------")
                print("---------2----------------")
                Member.objects.create(user = member_user, full_name = full_name, email = email ,avatar = avatar)
                return redirect('member_list')
    context = {
        'form':form,
    }
    return render(request, 'catalog/add_member.html', context=context)

def edit_member(request, pk):
    if not request.user.is_superuser:
        return redirect('login')
    member_instance = Member.objects.get(id=pk)
    form = EditMemberForm(instance=member_instance)
    if request.method == 'POST':
        form = EditMemberForm(request.POST, request.FILES, instance=member_instance)
        if form.is_valid():   
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            avatar = form.cleaned_data['avatar']
            form.save()
            return redirect('member_list')
    context = {
        'form':form,
    }
    return render(request, 'catalog/edit_member.html', context=context)

def member_detail(request, pk):
    if not request.user.is_superuser:
        return redirect('login')
    member_instance = Member.objects.get(id=pk)
    form = MemberDetailForm(instance= member_instance)
    context = {
        'form':form
    }
    return render(request, 'catalog/member_detail.html', context=context)  

class MemberDeleteView(DeleteView):
    model = Member
    template_name = 'catalog/confirm_delete.html'
    success_url = reverse_lazy('member_list')


# ----------------------------- Book issue CRUD views ------------------------------------------
def book_issue_list(request):
    book_issue = Issue.objects.all()
    return render(request, 'catalog/book_issued_list.html', {'book_issue': book_issue})

class BookIssueCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Issue
    template_name = "catalog/book_issue_form.html"
    fields = '__all__'
    success_message = "Book Issued added successfully."

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        print('Book added successfully!')
        return "Book Issued Successfully! "

    def get_context_data(self, **kwargs):
        data = super(BookIssueCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['items'] = BookIssueFormset(self.request.POST)
        else:
            data['items'] = BookIssueFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        items = context['items']
        with transaction.atomic():
            if items.is_valid():
                items.instance = form.save(commit=False)
                for i in items:
                    title=i.cleaned_data['title']
                    qt=i.cleaned_data['quantity']
                    book_quantity = BookEntry.objects.get(title=title)
                    if book_quantity.quantity < qt:
                        form.errors['value']='Your entered quantity exceeds book quantity'
                        return self.form_invalid(form)
                    else:
                        book_quantity.quantity -=qt
                        book_quantity.save()
                        form.save()
                        items.save()
                # sold_item.save()

        return super(BookIssueCreateView, self).form_valid(form)

    def get_initial(self):
        initial=super(BookIssueCreateView,self).get_initial()

        initial['member']=Member.objects.get(pk=self.kwargs['pk'])
        

        initial['member'] = Member.objects.get(pk=self.kwargs['pk'])
        # initial['member_id']=Member.objects.get(pk=self.kwargs['pk'])
 # 0f440745dcd3b74c34182e58054f66a3ac0842ec
        return initial

# def book_issue(request):
#     if not request.user.is_superuser:
#         return redirect('login')
#     form = BookIssueForm()
#     if request.method == 'POST':
#         form = BookIssueForm(request.POST, request.FILES)
#         if form.is_valid():
#             title=form.cleaned_data['issue_book_name']
#             qt=form.cleaned_data['quantity']
#             print(title)
#             print(qt)
#             book_quantity = BookEntry.objects.get(title=title)
#             if book_quantity.quantity < qt:
#                 form.errors['value']='Your entered quantity exceeds book quantity'
#                 return self.form_invalid(form)
#             else:
#                 book_quantity.quantity -=qt
#                 book_quantity.save()
#                 form.save()
#             return redirect('book_issue_list')
#     context = {
#         'form':form
#     }
#     return render(request, 'catalog/book_issue.html', context=context)

def book_issue_edit(request, issue_id):
    book_instance = Issue.objects.get(id=issue_id)
    form = IssueForm(request.POST,instance=book_instance)
    ItemFormset = inlineformset_factory(Issue, BookIssue, form=IssueForm, extra=0)
    if request.method == 'POST':
        formset = ItemFormset(data = request.POST, files = request.FILES, instance=book_instance)
        if form.is_valid():
            form.save()
            formset.save()
            return redirect('book_issue_list')
    else:
        form = IssueForm(instance=book_instance)
        formset = ItemFormset(instance=book_instance)

    return render(request, 'catalog/book_issue_edit.html', {'form': form, 'formset': formset})


class book_issue_detail(LoginRequiredMixin,DetailView):
    model = Issue
    template_name = 'catalog/book_issue_detail.html'

    def get_context_data(self, **kwargs):
        context = super(book_issue_detail, self).get_context_data(**kwargs)
        return context

class BookIssueDeleteView(DeleteView):
    model = Issue
    template_name = 'catalog/confirm_delete.html'
    success_url = reverse_lazy('book_issue_list')


# ----------------------------- Book return CRUD views ------------------------------------------
def book_return_list(request):
    book_return = BookReturn.objects.all()
    return render(request, 'catalog/book_return_list.html', {'book_return': book_return})

class BookReturnView(LoginRequiredMixin,DetailView,UpdateView):
    model = Issue
    fields='__all__'
    template_name = 'catalog/book_return_update.html'

    def get_context_data(self, **kwargs):
        data = super(BookReturnView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['items'] = BookIssueFormset(self.request.POST)
        else:
            data['items'] = BookIssueFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        full_name=context['object']
        user_id=User.objects.get(username=full_name)
        member_id = Member.objects.get(full_name=user_id)
        print(member_id)
        issue_id = Issue.objects.get(member_id=member_id)
        print(issue_id)
        items = context['items']
        with transaction.atomic():
            if items.is_valid():
                items.instance = form.save(commit=False)
                for i in items:
                    title = i.cleaned_data['title']
                    qt=i.cleaned_data['quantity']
                    isbn=i.cleaned_data['isbn']
                    print(title)
                    issue_item_id = BookIssue.objects.filter(issue_id_id=issue_id, isbn=isbn)
                    for i in issue_item_id:
                        i.quantity -= qt
                        i.save()
                        issued_item=BookEntry.objects.get(title=title)
                        issued_item.quantity +=qt
                        issued_item.save()
        return super(BookReturnView, self).form_valid(form)

# def book_return(request):
#     if not request.user.is_superuser:
#         return redirect('login')
#     form = BookReturnForm()
#     if request.method == 'POST':
#         form = BookReturnForm(request.POST, request.FILES)
#         if form.is_valid():
#             title=form.cleaned_data['title']
#             qt=form.cleaned_data['quantity']
#             print(title)
#             print(qt)
#             book_quantity = BookEntry.objects.get(title=title)
#             if book_quantity.quantity < qt:
#                 form.errors['value']='Your entered quantity exceeds book quantity'
#                 return self.form_invalid(form)
#             else:
#                 book_quantity.quantity += qt
#                 book_quantity.save()
#                 form.save()
#             return redirect('book_return_list')
#     context = {
#         'form':form
#     }
#     return render(request, 'catalog/add_book_return.html', context=context)

def book_return_edit(request, pk):
    if not request.user.is_superuser:
        return redirect('login')
    book_instance = BookReturn.objects.get(id=pk)
    form = BookReturnForm(instance=book_instance)
    if request.method == 'POST':
        form = BookReturnForm(data=request.POST, files=request.FILES, instance=book_instance)
        if form.is_valid():
            form.save()
            return redirect('book_return_list')
    context = {
        'form':form
    }
    return render(request, 'catalog/book_return_edit.html', context=context)

def book_return_detail(request, pk):
    if not request.user.is_superuser:
        return redirect('login')
    book_instance = BookReturn.objects.get(id=pk)
    form = BookReturnForm(instance= book_instance)
    context = {
        'form':form
    }
    return render(request, 'catalog/book_return_detail.html', context=context)  

class BookReturnDeleteView(DeleteView):
    model = BookReturn
    template_name = 'catalog/confirm_delete.html'
    success_url = reverse_lazy('book_return_list')


# ----------------------------- Book renew CRUD views ------------------------------------------
def book_renew_list(request):
    book_renew = BookRenew.objects.all()
    return render(request, 'catalog/book_renew_list.html', {'book_renew':book_renew})

def book_renew(request):
    if not request.user.is_superuser:
        return redirect('login')
    form = BookRenewForm()
    if request.method == 'POST':
        form = BookRenewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_renew_list')
    context = {
        'form':form
    }
    return render(request, 'catalog/add_book_renew.html', context=context)

def book_renew_edit(request, pk):
    if not request.user.is_superuser:
        return redirect('login')
    book_instance = BookRenew.objects.get(id=pk)
    form = BookRenewForm(instance=book_instance)
    if request.method == 'POST':
        form = BookRenewForm(data=request.POST, files=request.FILES, instance=book_instance)
        if form.is_valid():
            form.save()
            return redirect('book_renew_list')
    context = {
        'form':form
    }
    return render(request, 'catalog/book_renew_edit.html', context=context)

def book_renew_detail(request, pk):
    if not request.user.is_superuser:
        return redirect('login')
    book_instance = BookRenew.objects.get(id=pk)
    form = BookRenewForm(instance= book_instance)
    context = {
        'form':form
    }
    return render(request, 'catalog/book_renew_detail.html', context=context)  

class BookRenewDeleteView(DeleteView):
    model = BookRenew
    template_name = 'catalog/confirm_delete.html'
    success_url = reverse_lazy('book_renew_list')
