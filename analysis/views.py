from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from db import connect
from mysql.connector.cursor import MySQLCursorAbstract
from rest_framework.decorators import api_view
import constants
import datetime
from collections import defaultdict
import calendar

data = {
    "2023" : [
        {
            "month" : "January",
            "transactions": {"description": "chipotle", "amount" : 500.0, "type": "Bills and Transfers", "count": 3},
        },
        {}
    ],
    "2024" : [
        {},
        {}
    ]
}

transaction_test = [(2, datetime.date(2024, 1, 10), 'Purchase', 'Uber Trip Help.Uber.Com', 'test2', 20.98), (3, datetime.date(2024, 1, 10), 'Purchase', 'Uber Trip Help.Uber.Com', 'test1', 20.95), (4, datetime.date(2024, 1, 12), 'Purchase', 'Albertsons Irvine', 'test2', 5.39), (6, datetime.date(2024, 1, 13), 'Purchase', 'Joes Italian Ice Anaheim', 'test2', 8.36), (7, datetime.date(2024, 1, 14), 'Recurring Payment', 'Spotify', 'test1', 5.99), (8, datetime.date(2024, 1, 15), 'Zelle From Roksana Nassir', 'Electric Bill', 'test2', 14.39), (9, datetime.date(2024, 1, 15), 'Purchase', 'Albertsons Irvine', 'test1', 67.07), (10, datetime.date(2024, 1, 10), 'Purchase', 'Uber Trip Help.Uber.Com', 'test2', 20.98), (11, datetime.date(2024, 1, 16), 'Purchase', 'NOut Irvine Irvine', 'test2', 11.96), (12, datetime.date(2024, 1, 10), 'Purchase', 'Uber Trip Help.Uber.Com', 'test1', 20.95)]

num_to_month ={
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}


# group them first by name, then by 
def group(transaction_data):
    grouped_transactions = {}
    for id, date, type, description, category, amount in transaction_data:
        if description not in grouped_transactions:
            grouped_transactions[description] = [date, type, description, category, amount, 1]
        else:
            grouped_transactions[description][4] += amount
            grouped_transactions[description][5] += 1
    return grouped_transactions



def get_transactions_year(connector, cursor: MySQLCursorAbstract, year: int):
    year_data = {
    }

    # for id, startDate, endDate, startAmount, endAmount, dateYear in data:
    # start_date = f"{year}-01-01"
    # end_date = f"{year}-12-31"
    for month in range(1, 13):
        start_date = f'{year}-{month}-01'
        end_day = calendar.monthrange(year, month)[1]
        end_date = f'{year}-{month}-{end_day}'

        sql = f"SELECT * FROM transaction_transaction WHERE date >= '{start_date}' AND '{end_date}' >= date LIMIT 10"
        # print(sql)
        cursor.execute(sql)
        transactions = cursor.fetchall()
        grouped_transactions = group(transactions)
        month_data = {}

        month_data["month"] = num_to_month[month]
        month_data["transactions"] = grouped_transactions
        print(month_data)
        if str(year) not in year_data.keys():
            year_data[str(year)] = [month_data]
        else:
            year_data[str(year)].append(month_data)
    print(year_data)

    return year_data

def get_years(connector, cursor: MySQLCursorAbstract):
    sql = f"SELECT DISTINCT year FROM upload_pdf_months"
    cursor.execute(sql)
    data = [tup[0] for tup in cursor.fetchall()]
    # print(data)
    return data, connector, cursor

@csrf_exempt
@api_view(["GET"])
def get_analysis(request: HttpRequest):
    query_type = request.GET.get('type')

    connector, cursor = connect(constants.HOST, constants.USER, constants.PASSWORD)
    sql = "use budget_app"
    cursor.execute(sql)
    
    if query_type == "list-years":
        data, connector, cursor = get_years(connector, cursor)
        return JsonResponse({"status": "Success", "years": data})
    elif query_type == "year-data":
        year = int(request.GET.get('year'))
        json = get_transactions_year(connector, cursor, year)
        return JsonResponse({"status": f"Success, grabbing data for year {year}", "data": json})
    else:
        return JsonResponse({"status": "Error, not a valid GET to /analysis", "transactions": []})