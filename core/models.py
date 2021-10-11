from secrets import token_hex

from django.db import models
from django.db.models.aggregates import Count
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import localtime
from django.urls.base import reverse_lazy
from django.db.models import Count


class CommonPersonFields(models.Model):
    '''
        Base Fields for (Author, Reader)
    '''
    name = models.CharField(_("name"), max_length=150)
    phone = models.CharField(_("phone"), max_length=20, unique=True)
    email = models.EmailField(_("email"), max_length=254, unique=True)
   
    class Meta:
        ordering = ['-id']
        abstract = True
    
    def __str__(self) -> str:
        return self.name
    
    def _normalize_name(self, name):
        return self._normalize_str(name)

    def save(self, *args, **kwargs) -> None:
        self.name = self._normalize_name(self.name)
        self.email = self._normalize_email(self.email)
        return super().save(*args, **kwargs)
  
    def _normalize_email(self, email):
        return self._normalize_str(email)
    
    def _normalize_str(self, str_value):
        return str_value.lower().strip()

    @property
    def books_no(self):
        return self.books.aggregate(no=Count('id')).get('no', 0)

         
class Author(CommonPersonFields):
    '''
        Create Author model in db
    '''
    @property
    def readers(self):
        '''
            Returns reader as str
        '''
        return {
                str(reader)
                for book in self.books.all()
                for reader in book.readers.all() 
        }
    
    @property
    def readers_as_obj(self):
        '''
            Returns the reader model object
        '''
        return {
                reader
                for book in self.books.all()
                for reader in book.readers.all() 
        }
    def get_absolute_url(self):
        return reverse_lazy("core:author", kwargs={"pk": self.pk})


class Reader(CommonPersonFields):
    '''
        Create Reader model in db
    '''

    def get_absolute_url(self):
       return reverse_lazy("core:reader", kwargs={"pk": self.pk})

    @property
    def authors(self):
        return {
            str(book.author) for book in self.books.author
        }


class Book(models.Model):
    '''
        Create Book model in db
    '''

    ## Bad practice i will find another way to do it !!
    def token_hex_modified():
        '''
            limit length to 8bytes
        '''
        return  token_hex(8)

    title = models.CharField(_("book title"), max_length=150)
    readers = models.ManyToManyField("Reader", verbose_name=_("reader"), related_name='books', )
    author = models.ForeignKey("Author", verbose_name=_("author"), on_delete=models.CASCADE, related_name='books')
    created_at = models.DateTimeField(_("created at"), default=localtime)
    serial_no = models.CharField(_("serial"), max_length=50, default= token_hex_modified, unique=True)
 
    class Meta:
        ordering = ['-id']
        unique_together = ('title', 'author')

    def get_absolute_url(self):
       return reverse_lazy("core:book", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return '{title} by {author}'.format(author=self.author, title=self.title)
    
    def _normalize_title(self, title):
        return self._normalize_str(title)
    
    def _normalize_str(self, str_value):
        return str_value.lower().strip()

    def save(self, *args, **kwargs) -> None:
        self.title = self._normalize_title(self.title)
        return super().save(*args, **kwargs)