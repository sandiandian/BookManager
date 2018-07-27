from django.conf.urls import url

from .views import *


urlpatterns = [
    url(r'addbook', Addbook.as_view(), name='addbook'),
    url(r'addauthor', Addauthor.as_view(), name='addauthor'),
    url(r'addpublisher', Addpublisher.as_view(), name='addpublisher'),
    url(r'addtypebook', Addtypebook.as_view(), name='addtypebook'),
    url(r'author_create_details', Author_Create_Details.as_view(), name='author_create_details'),
    url(r'create_details', Create_Details.as_view(), name='create_details'),
    url(r'book_del', Book_Del.as_view(), name='book_del'),
    url(r'author_del', Author_Del.as_view(), name='author_del'),
    url(r'publisherdel', Publisher_del.as_view(), name='publisherdel'),
    url(r'typebookdel', TypeBook_del.as_view(), name='typebookdel'),
    url(r'edit_book/(?P<book_id>\d+)/$', Edit_Book.as_view(), name='edit_book'),
]