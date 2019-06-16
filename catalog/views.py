from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
import datetime

from .models import *
from .forms import RenewBookForm


def index(request):
    # amount of books and book instances
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # available books
    num_instances_available = BookInstance.objects.filter(status__iexact='a').count()
    num_authors = Author.objects.count()

    num_genres = Genre.objects.count()
    rand_book = get_random_book

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {'num_books': num_books, 'num_instances': num_instances,
               'num_instances_available': num_instances_available,
               'num_authors': num_authors, 'num_genres': num_genres,
               'rand_book': rand_book, 'num_visits': num_visits,}
    return render(request, 'catalog/index.html', context)


@permission_required('catalog.can_mark_returned')
def renew_bookinst(request, pk):
    book_inst = get_object_or_404(BookInstance, pk=pk)
    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_inst.due_back = form.cleaned_data['due_back']
            book_inst.save()
            return HttpResponseRedirect(reverse('catalog:borrowed_all_url'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'due_back': proposed_renewal_date,})
    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst': book_inst})


class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    paginate_by = 15


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book


class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    paginate_by = 15


class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author
    slug_field = 'id'
    slug_url_kwarg = 'id'


class PublisherListView(LoginRequiredMixin, generic.ListView):
    model = Publisher
    paginate_by = 15


class PublisherDetailView(LoginRequiredMixin, generic.DetailView):
    model = Publisher
    slug_field = 'id'
    slug_url_kwarg = 'id'


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10


    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class BorrowedBooksByUsersListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/borrowed_all.html'
    paginate_by = 10
    permission_required = 'catalog.can_mark_returned'

    queryset = BookInstance.objects.exclude(borrower=None)


class UserListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    model = User
    paginate_by = 10
    template_name = 'catalog/auth/user_list.html'
    permission_required = 'catalog.can_lookup_users'

    queryset = User.objects.order_by('username')


class UserDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    model = User
    permission_required = 'catalog.can_lookup_users'
    template_name = 'catalog/auth/user_detail.html'
    slug_url_kwarg = 'username'
    slug_field = 'username'


class GenreListView(LoginRequiredMixin, generic.ListView):
    model = Genre
    paginate_by = 15


class GenreDetailView(LoginRequiredMixin, generic.DetailView):
    model = Genre
    slug_field = 'name'
    slug_url_kwarg = 'name'


class AuthorCreate(PermissionRequiredMixin, generic.CreateView):
    model = Author
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'


class AuthorUpdate(PermissionRequiredMixin, generic.UpdateView):
    model = Author
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'


class AuthorDelete(PermissionRequiredMixin, generic.DeleteView):
    model = Author
    success_url = reverse_lazy('catalog:authors_url')
    template_name_suffix = '_delete'
    permission_required = 'catalog.can_mark_returned'


class GenreCreate(PermissionRequiredMixin, generic.CreateView):
    model = Genre
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'
    success_url = reverse_lazy('catalog:genres_url')


class GenreUpdate(PermissionRequiredMixin, generic.UpdateView):
    model = Genre
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'


class GenreDelete(PermissionRequiredMixin, generic.DeleteView):
    model = Genre
    success_url = reverse_lazy('catalog:genres_url')
    template_name_suffix = '_delete'
    permission_required = 'catalog.can_mark_returned'


class PublisherCreate(PermissionRequiredMixin, generic.CreateView):
    model = Publisher
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'
    success_url = reverse_lazy('catalog:publishers_url')


class PublisherUpdate(PermissionRequiredMixin, generic.UpdateView):
    model = Publisher
    fields = ('name', 'url',)
    permission_required = 'catalog.can_mark_returned'


class PublisherDelete(PermissionRequiredMixin, generic.DeleteView):
    model = Publisher
    template_name_suffix = '_delete'
    permission_required = 'catalog.can_mark_returned'
    success_url = reverse_lazy('catalog:publishers_url')


class BookCreate(PermissionRequiredMixin, generic.CreateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'
    success_url = reverse_lazy('catalog:books_url')


class BookUpdate(PermissionRequiredMixin, generic.UpdateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'


class BookDelete(PermissionRequiredMixin, generic.DeleteView):
    model = Book
    success_url = reverse_lazy('catalog:books_url')
    template_name_suffix = '_delete'
    permission_required = 'catalog.can_mark_returned'


class RegistrationFormView(generic.edit.FormView):
    form_class = UserCreationForm
    success_url = ""
    template_name = 'registration/register.html'

    def form_valid(self, form):
        form.save()
        return super(RegistrationFormView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('login')