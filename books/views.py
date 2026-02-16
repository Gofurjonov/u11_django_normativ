from django.shortcuts import render,redirect,get_object_or_404
from books.forms import BookModelForm

from .models import Book


def book_list(request):
    books = Book.objects.all()
    return render(request, "books/book_list.html", {'books':books})

def book_create(request):
    if request.method == 'POST':
        form = BookModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookModelForm()
    return render(request, 'books/book_form.html', {'form': form})


def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = BookModelForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookModelForm(instance=book)

    return render(request, 'books/book_form.html', {'form': form, 'title': 'Tahrirlash'})


def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})