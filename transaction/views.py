from django.shortcuts import render
from rest_framework import viewsets
from .serializers import TransactionSerializer
from .models import Transaction
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

class TransactionView(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
