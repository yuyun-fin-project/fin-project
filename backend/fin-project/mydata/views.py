from django.shortcuts import render
from .utils.api_clients.mydata_api import get_card_list, get_card_approval
from .utils.data_processors.my_data_cleaner import my_data_cleaner
import requests
# from .serializers import DepositOptionSerializer, DepositProductsSerializer
# from .models import DepositProducts, DepositOptions
from openai import OpenAI
from django.conf import settings
import os


# Create your views here.
@api_view(['POST'])
def get_mydata(request):
    card_list = get_card_list(request)
    card_list, jwt_token = my_data_cleaner(card_list)
    for card in card_list:
        card_approval = get_card_approval(jwt_token, card['card_id'])
    
    return Response(card_approval)

