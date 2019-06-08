from django.shortcuts import render
from .models import *
from django.views import generic


def index(request):
    # amount of books and book instances
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # available books
    num_instances_available = BookInstance.objects.filter(status__iexact='a').count()
    num_authors = Author.objects.count()

    num_genres = Genre.objects.count()
    rand_book = get_random_book

    context = {'num_books': num_books, 'num_instances': num_instances,
               'num_instances_available': num_instances_available,
               'num_authors': num_authors, 'num_genres': num_genres,
               'rand_book': rand_book}
    return render(request, 'catalog/index.html', context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 15
    # def get_queryset(self):
    #     return Book.objects.filter(title__icontains='а')[:5]

    # def get_context_data(self, **kwargs):
    #     context = super(BookListView, self).get_context_data(**kwargs)
    #     context['some_data'] = 'its an example'
    #     return context


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 5


class AuthorDetailView(generic.DetailView):
    model = Author
    slug_field = 'id'
    slug_url_kwarg = 'id'


class PublisherListView(generic.ListView):
    model = Publisher
    paginate_by = 5


class PublisherDetailView(generic.DetailView):
    model = Publisher
    slug_field = 'id'
    slug_url_kwarg = 'id'

    #queryset =