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


# group_by_name them first by name, then by 
def group_by_name(transaction_data):
    grouped_transactions = {}
    for id, date, type, description, category, amount in transaction_data:
        if description not in grouped_transactions:
            grouped_transactions[description] = [date, type, description, category, amount, 1]
        else:
            grouped_transactions[description][4] += round(amount, 2)
            grouped_transactions[description][5] += 1
    return grouped_transactions

def group_by_category(transaction_data, group_type):
    grouped_transactions = defaultdict(int)
    for id, date, type, description, category, amount in transaction_data:
        value = 0
        if group_type == "total-cost":
            value = round(amount, 2)
        elif group_type == "total-count":
            value = 1
        grouped_transactions[category] += value

    return grouped_transactions

# all years set as -1
def get_transactions(connector, cursor: MySQLCursorAbstract, year: int, group_by: str):
    year_data = {}

    for month in range(1, 13):
        start_date = f'{year}-{month}-01'
        end_day = calendar.monthrange(year, month)[1]
        end_date = f'{year}-{month}-{end_day}'

        if year < 0:
            sql = f"SELECT * FROM transaction_transaction WHERE MONTH(date) = '{month}'"
        else:
            sql = f"SELECT * FROM transaction_transaction WHERE date >= '{start_date}' AND '{end_date}' >= date LIMIT 10"

        cursor.execute(sql)
        transactions = cursor.fetchall()
        grouped_transactions = None
        print(transactions)
        if group_by == "name":
            grouped_transactions = group_by_name(transactions)
        elif group_by == "category":
            grouped_transactions = group_by_category(transactions)
        
        
        month_data = {}
        month_data["month"] = num_to_month[month]
        for t in grouped_transactions:
            month_data[t] = grouped_transactions[t]
        # print(month_data)
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

def get_categories_year(connector, cursor: MySQLCursorAbstract, year: int, month: int, group_type: str):
    """
        Takes a year(-1 or an +int) and a type (count or cost), returns the data for all relevant years grouped by month
    """
    year_data = defaultdict(int)
    months = []
    if month == -1:
        months = list(range(1, 13))
    else:
        months = [month]
    # months = [i for i in ]
    for month in months:
        start_date = f'{year}-{month}-01'
        end_day = calendar.monthrange(year, month)[1]
        end_date = f'{year}-{month}-{end_day}'

        if year < 0:
            sql = f"SELECT * FROM transaction_transaction WHERE MONTH(date) = '{month}'"
        else:
            sql = f"SELECT * FROM transaction_transaction WHERE date >= '{start_date}' AND '{end_date}' >= date LIMIT 10"

        cursor.execute(sql)
        transactions = cursor.fetchall()

        for id, date, type, description, category, amount in transactions:
            print(description, category, amount)
            if group_type == "total-count":
                year_data[category] += 1
            elif group_type == "total-cost":
                year_data[category] += amount
            
        # grouped_transactions = None
        # grouped_transactions = group_by_category(transactions, type)
        
        # month_data = {}
        # month_data["month"] = num_to_month[month]
        # for t in grouped_transactions:
        #     month_data[t] = grouped_transactions[t]
        # # print(month_data)
        # if str(year) not in year_data.keys():
        #     year_data[str(year)] = [month_data]
        # else:
        #     year_data[str(year)].append(month_data)
    print(year_data)

    return year_data

# fix "data"
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
        json = get_transactions(connector, cursor, year, "name")
        return JsonResponse({"status": f"Success, grabbing data for year {year}", "data": json})
    elif query_type == "category-data":
        year = int(request.GET.get('year'))
        month = int(request.GET.get('month'))
        type = request.GET.get('group-type')
        
        json = get_categories_year(connector, cursor, year, month, type)
        
        return JsonResponse({"status": f"Success, grabbing data for year: {year} month: {month} type: {type}", "transactions": json})
    else:
        return JsonResponse({"status": "Error, not a valid GET to /analysis", "transactions": []})