from django.urls import path
from core import views

'''
    urls of apps
    @naming convenvsion
    {project}:{app}-{action}, [pk, ]
'''

# auhtor_router = DefaultRouter()
# auhtor_router.register('')

urlpatterns = [
    #Author Urls
    path('author/', views.AuthorCreate().as_view(), name='author-create'),
    path('author/<int:pk>/update', views.AuthorUpdate().as_view(), name='author-update'),
    path('author/<int:pk>/delete', views.AuthorDelete().as_view(), name='author-delete'),
    path('author/<int:pk>/', views.AuthorGet().as_view(), name='author-get'),
    path('authors/', views.AuthorList().as_view(), name='author-list'),

    #Book Urls
    path('book/', views.BookCreate().as_view(), name='book-create'),
    path('book/<int:pk>/update', views.BookUpdate().as_view(), name='book-update'),
    path('book/<int:pk>/delete', views.BookDelete().as_view(), name='book-delete'),
    path('book/<int:pk>/', views.BookGet().as_view(), name='book-get'),
    path('books/', views.BookList().as_view(), name='book-list'),


    #Reader Urls
    path('reader/', views.ReaderCreate().as_view(), name='reader-create'),
    path('reader/<int:pk>/update', views.ReaderUpdate().as_view(), name='reader-update'),
    path('reader/<int:pk>/delete', views.ReaderDelete().as_view(), name='reader-delete'),
    path('reader/<int:pk>/', views.ReaderGet().as_view(), name='reader-get'),
    path('readers/', views.ReaderList().as_view(), name='reader-list'),
    path('reader/<int:pk>/books/delete', views.ReaderBooksDelete().as_view(), name='reader-books_delete'),
]
