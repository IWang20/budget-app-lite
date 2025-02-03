from django.shortcuts import render
from rest_framework import viewsets
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, JsonResponse
from .forms import UploadFileForm
from pypdf import PdfReader
from django.views.decorators.csrf import csrf_exempt
from parse_pdfs import parseFile
from db import connect
import constants
from mysql.connector.cursor import MySQLCursorAbstract
from dateutil import parser


def insert_fee_period(connector, cursor: MySQLCursorAbstract, data):
    connector.database = constants.DATABASE
    sql = f"INSERT INTO upload_pdf_months (year, start_date, end_date, beginning_balance, ending_balance) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (parser.parse(data["startDate"]).year, parser.parse(data["startDate"]).date(), parser.parse(data["endDate"]).date(), data["beginningBalance"], data["endingBalance"]))

    print(f"Inserted Period {data['startDate']} - {data['endDate']}")
    connector.commit()

def handle_uploaded_pdf(f):
    pdf_data, total, added = parseFile(f)
    
    connector, cursor = connect(constants.HOST, constants.USER, constants.PASSWORD)
    insert_fee_period(connector, cursor, pdf_data)


    print(f"{pdf_data['startDate']} - {pdf_data['endDate']} : {total} transactions, {added} transactions added")
    # print(f"{pdf_data["startDate"]}")
    transactions = sorted(pdf_data["transactions"], key=lambda x: x[0])
    return transactions

@csrf_exempt
def upload_pdf(request: HttpRequest):
    if request.method == "POST":
        transactions = handle_uploaded_pdf(request.FILES["pdf"])
        # print(transactions)
        return JsonResponse({"status": "File Uploaded", "transactions": transactions})
    else:
        form = UploadFileForm()
    return JsonResponse({"status": "Error, not a valid POST to /upload_pdf", "transactions": []})