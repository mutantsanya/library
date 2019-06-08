from django.db import models
from django.urls import reverse
import uuid
from random import randint
from django.db.models import Max
from django.utils.text import slugify
from time import time


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


class Author(models.Model):
    """
    model representing authors of the book
    """
    first_name = models.CharField('имя', max_length=70)
    second_name = models.CharField('фамилия', max_length=70)
    about = models.TextField('об авторе', max_length=1000, blank=True, null=True)
    email = models.EmailField('email', blank=True, null=True)
    date_of_birth = models.DateField('дата рождения', blank=True, null=True)
    date_of_death = models.DateField('дата смерти', blank=True, null=True)

    def __str__(self):
        """
        string for representing the model object
        """
        return '{0} {1}'.format(self.second_name, self.first_name)
        # return f'{self.second_name} {self.first_name}'

    def get_absolute_url(self):
        """
        return the url to a particular author
        """
        return reverse('catalog:author_detail_url', kwargs={'id': str(self.id)})

    class Meta:
        """
        meta data about table
        """
        ordering = ('second_name',)


class Genre(models.Model):
    """
    model representing a book genre (science fiction, non fiction etc)
    """
    name = models.CharField(max_length=150,
                            help_text='Enter a book genre',
                            unique=True)

    def __str__(self):
        """
        string for representing the model object
        """
        return self.name


class Book(models.Model):
    """
    model representing a book
    """
    title = models.CharField(max_length=150, help_text='Введите название книги',
                             verbose_name='название')
    slug = models.SlugField(max_length=150, blank=True, unique=True, allow_unicode=True)
    author = models.ManyToManyField(Author, verbose_name='автор')
    summary = models.TextField(max_length=1000, help_text='Введите краткое описание книги',
                               verbose_name='описание')
    isbn = models.CharField(max_length=13, verbose_name='ISBN',
                            help_text='13 символов <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text='Выберите жанры для этой книги',
                                   verbose_name='жанр')
    language = models.ForeignKey('Language', on_delete=models.PROTECT,
                                 help_text='Выберите язык этой книги', verbose_name='язык')
    publisher = models.ForeignKey('Publisher', on_delete=models.SET_NULL, null=True,
                                  verbose_name='издательство')
    pub_date = models.DateField('дата публикации', blank=True, null=True)

    def display_genre(self):
        """
        creates a string for the genre (required to display genre in admin)
        """
        return ', '.join([genre.name for genre in self.genre.order_by('name')[:3]])

    display_genre.short_description = 'жанр'

    def display_author(self):
        """
        same shit for author in admin
        """
        return ', '.join(
            [str(author.second_name + ' ' + author.first_name) for author in self.author.order_by('second_name')])

    display_author.short_description = 'автор'

    def __str__(self):
        """
        string for representing the model object
        """
        return '{}'.format(self.title)

    def get_absolute_url(self):
        """
        return the url to access a particular book instance
        """
        return reverse('catalog:book_detail_url', kwargs={'slug': str(self.slug)})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gen_slug(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ('title',)


def get_random_book():
    max_id = Book.objects.all().aggregate(max_id=Max('id'))['max_id']
    while True:
        pk = randint(1, max_id)
        book = Book.objects.filter(pk=pk).first()
        if book:
            return book


class Language(models.Model):
    """
    model representing languages of books
    """
    name = models.CharField('название', max_length=20, unique=True)
    code = models.CharField('ISO 639', max_length=2, unique=True)

    def __str__(self):
        """
        string for representing the model object
        """
        return '{} - {}'.format(self.name, self.code)

    class Meta:
        ordering = ('name',)


class Publisher(models.Model):
    """
    model representing information about book publisher
    """
    name = models.CharField('название', max_length=50, unique=True)
    address = models.CharField('адрес', max_length=100)
    city = models.CharField('город', max_length=50)
    state_province = models.CharField('штат/область', max_length=50)
    country = models.CharField('страна', max_length=50)
    url = models.URLField('сайт', blank=True, null=True)

    def __str__(self):
        """
        string for representing the model object
        """
        return self.name

    def get_absolute_url(self):
        """
        get access url to a particular publisher
        """
        return reverse('catalog:publisher_detail_url', kwargs={'id': str(self.id)})



class BookInstance(models.Model):
    """
    model representing a specific copy of a book
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Уникальный ID для конкретного экземпляра книги в библиотеке',
                          auto_created=True, verbose_name='UUID', editable=False)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, verbose_name='книга')
    due_back = models.DateField('дата возврата', null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Тех. обслуживание'),
        ('o', 'Выдана'),
        ('a', 'Доступна'),
        ('r', 'Зарезервирована'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m',
                              help_text='Доступность книги', verbose_name='статус')

    def __str__(self):
        return '{} {}'.format(self.id, self.book.title)

    class Meta:
        ordering = ('due_back',)
