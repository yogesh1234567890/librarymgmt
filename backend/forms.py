from django import forms
from .models import *

class BookForm(forms.ModelForm):
    class Meta:
        model = BookEntry
        fields = '__all__'


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
    }))
    password = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
        'type': 'password'
    }))

class BookAddForm(forms.ModelForm):
    class Meta:
        model = BookEntry
        fields = '__all__'
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'title',
        'data-val': 'true',
        'data-val-required': 'Please enter title of the book',
    }))
    author = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'author',
        'data-val': 'true',
        'data-val-required': 'Please enter author name',
    }))
    isbn = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'id': 'isbn',
        'data-val': 'true',
        'data-val-required': 'Please 13 digit isbn',
    }))
    summary = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'summary',
        'data-val': 'true',
        'data-val-required': 'Please enter book summary',
    }))
    genre = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'genre',
        'data-val': 'true',
        'data-val-required': 'example: science, history, Programming, Comic',
    }))
    language = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'language',
        'data-val': 'true',
        'data-val-required': 'Please enter book return in language',
    }))
    total_copies = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'id': 'total_copies',
        'data-val': 'true',
        'data-val-required': 'Please enter total copies',
    }))
    available_copies = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'id': 'available_copies',
        'data-val': 'true',
        'data-val-required': 'Please enter available copies',
    }))
    pic = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'form-control',
        'id': 'pic',
        'data-val': 'true',
        'data-val-required': 'Please enter available copies',
    }))
    published_year = forms.DateField(
        widget=forms.DateInput(attrs={
        'type': 'date',
        'class': 'form-control',
        'data-val-required': 'Please enter book published year',    
    }))

class BookIssueForm(forms.ModelForm):
    class Meta:
        model = BookIssue
        fields = '__all__'
        exclude = ['issue_date']
        widgets = {
            'issue_book_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'issue_book_name'}),
            'isbn': forms.Select(attrs={'class': 'form-control', 'id': 'isbn'}),
            'member_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'member_name'}),
            'member_id': forms.Select(attrs={'class': 'form-control', 'id': 'member_id'}),
        }

class BookReturnForm(forms.ModelForm):
    class Meta:
        model = BookReturn
        exclude = ['return_date', 'created_at']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'id': 'title'}),
            'isbn': forms.Select(attrs={'class': 'form-control', 'id': 'isbn'}),
            'member_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'member_name'}),
            'member_id': forms.Select(attrs={'class': 'form-control', 'id': 'member_id'}),
        }

class BookRenewForm(forms.ModelForm):
    class Meta:
        model = BookRenew
        fields = '__all__'
        exclude = ['renew_date', 'created_at']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'id': 'title'}),
            'isbn': forms.Select(attrs={'class': 'form-control', 'id': 'isbn'}),
            'member_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'member_name'}),
            'member_id': forms.Select(attrs={'class': 'form-control', 'id': 'member_id'}),
        }


class AddMemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'
        exclude = ('user',)
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'first_name',
        'data-val': 'true',
        'data-val-required': 'Please enter first name',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'last_name',
        'data-val': 'true',
        'data-val-required': 'Please enter last name',
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'email',
        'data-val': 'true',
        'data-val-required': 'Please enter email',
    }))
    avatar = forms.ImageField(widget=forms. FileInput(attrs={
        'class': 'form-control',
        'id': 'email',
        'data-val': 'true',
        'data-val-required': 'Please enter email',
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'username',
        'data-val': 'true',
        'data-val-required': 'Please enter username',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'password',
        'data-val': 'true',
        'data-val-required': 'Please enter password',
    }))
    retype_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'retype_password',
        'data-val': 'true',
        'data-val-required': 'Please enter retype_password',
    }))

class EditMemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'
        exclude = ('user',)
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'first_name',
        'data-val': 'true',
        'data-val-required': 'Please enter first name',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'last_name',
        'data-val': 'true',
        'data-val-required': 'Please enter last name',
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'email',
        'data-val': 'true',
        'data-val-required': 'Please enter email',
    }))
    avatar = forms.ImageField(widget=forms. FileInput(attrs={
        'class': 'form-control',
        'id': 'email',
        'data-val': 'true',
        'data-val-required': 'Please enter email',
    }))