from django.urls import path
from .views import  book_list, add_book, login_page, logout_page, member_list, book_issue_list, book_issue, add_member,edit_book, book_issue_edit
urlpatterns = [
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('book_list/', book_list, name='book_list'),
    path('member_list/', member_list, name='member_list'),
    path('book_issue_list/', book_issue_list, name='book_issue_list'),
    path('book_issue/', book_issue, name='book_issue'),
    path('add_book/', add_book, name='add_book'),
    path('add_member', add_member, name='add_member'),
    path('edit_book/<str:pk>/', edit_book, name='edit_book'),
    path('book_issue_edit/<int:pk>/', book_issue_edit, name='book_issue_edit'),
]