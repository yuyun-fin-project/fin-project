from django.shortcuts import render
from .api_clients.mydata_api import api_test
# from .data_processors import my_data_cleaner
import requests
from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
# from .serializers import DepositOptionSerializer, DepositProductsSerializer
# from .models import DepositProducts, DepositOptions
from openai import OpenAI
from django.conf import settings
import os


# Create your views here.
def get_mydata(request):
    card_list = api_test(request)
    return card_list