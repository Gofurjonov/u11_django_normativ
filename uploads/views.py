from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Document
from .forms import DocumentForm


@login_required
def upload_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.uploaded_by = request.user
            document.save()
            messages.success(request, f"'{document.title}' muvaffaqiyatli yuklandi!")
            return redirect('uploads:upload_list')
    else:
        form = DocumentForm()

    return render(request, 'uploads/upload.html', {'form': form})


@login_required
def file_list(request):
    # Faqat aktiv (o'chirilmagan) fayllar
    documents = Document.objects.filter(uploaded_by=request.user)

    search_query = request.GET.get('q', '')
    if search_query:
        documents = documents.filter(title__icontains=search_query)

    paginator = Paginator(documents, 10)
    page_number = request.GET.get('page', 1)
    documents = paginator.get_page(page_number)

    return render(request, 'uploads/list.html', {
        'documents': documents,
        'search_query': search_query
    })


@login_required
def delete_file(request, pk):
    # all_objects dan olamiz (o'chirilganlar ham bo'lishi mumkin)
    document = get_object_or_404(Document.all_objects, pk=pk, uploaded_by=request.user)

    if request.method == 'POST':
        title = document.title
        # Soft delete (faqat is_deleted=True qiladi)
        document.delete()
        messages.success(request, f"'{title}' o'chirildi!")
        return redirect('uploads:upload_list')

    return render(request, 'uploads/confirm_delete.html', {'document': document})


@login_required
def hard_delete_file(request, pk):
    # Butunlay o'chirish (faylni ham o'chiradi)
    document = get_object_or_404(Document.all_objects, pk=pk, uploaded_by=request.user)

    if request.method == 'POST':
        title = document.title
        document.hard_delete()
        messages.success(request, f"'{title}' butunlay o'chirildi!")
        return redirect('uploads:upload_list')

    return render(request, 'uploads/confirm_hard_delete.html', {'document': document})


@login_required
def restore_file(request, pk):
    """O'chirilgan faylni tiklash"""
    document = get_object_or_404(Document.all_objects, pk=pk, uploaded_by=request.user, is_deleted=True)

    if request.method == 'POST':
        document.restore()
        messages.success(request, f"'{document.title}' tiklandi!")
        return redirect('uploads:upload_list')

    return render(request, 'uploads/confirm_restore.html', {'document': document})