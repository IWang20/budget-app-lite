from django.shortcuts import render
from rest_framework import viewsets
from django.http import HttpResponseRedirect, HttpResponse
from .forms import UploadFileForm
from pypdf import PdfReader
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def handle_uploaded_pdf(f):
    reader = PdfReader(f)
    print("reading file")
    print(reader.pages[0].extract_text()[:100])

@csrf_exempt
def upload_pdf(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_pdf(request.FILES["file"])
            return HttpResponse("success")
    else:
        form = UploadFileForm()
    return HttpResponse("um")