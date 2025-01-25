from django.shortcuts import render
from rest_framework import viewsets
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, JsonResponse
from .forms import UploadFileForm
from pypdf import PdfReader
from django.views.decorators.csrf import csrf_exempt
from parse_pdfs import parseFile

# Create your views here.

def handle_uploaded_pdf(f):
    pdf_data, total, added = parseFile(f)

    print(f"{pdf_data['startDate']} - {pdf_data['endDate']} : {total} transactions, {added} transactions added")
    # print(f"{pdf_data["startDate"]}")
    transactions = sorted(pdf_data["transactions"], key=lambda x: x[0])
    return transactions

@csrf_exempt
def upload_pdf(request: HttpRequest):
    if request.method == "POST":
        # form = UploadFileForm(request.POST, request.FILES)
        # print(f"POST -- {request.POST}, {request.FILES}, {request.content_type}\nForm: {form.file}")
        # if form.is_valid():
        #     handle_uploaded_pdf(request.FILES["file"])
        #     return HttpResponse("success")
        # else:
        #     return HttpResponse("invalid form")
        transactions = handle_uploaded_pdf(request.FILES["pdf"])
        print(transactions)
        return JsonResponse({"status": "File Uploaded", "transactions": transactions})
    else:
        form = UploadFileForm()
    return JsonResponse({"status": "Error, not a valid POST to /upload_pdf", "transactions": []})