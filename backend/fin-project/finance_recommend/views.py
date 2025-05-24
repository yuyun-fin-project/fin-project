from .utils.spot.spot_api import spot_api
from rest_framework.response import Response
from django.shortcuts import render
from .utils.api_call import api_call
from .utils.data_preprocessing import data_preprocessing
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
# from .serializers import DepositOptionSerializer, DepositProductsSerializer
# from .models import DepositProducts, DepositOptions
from django.conf import settings
import os


# Create your views here.
def get_spot(request):
    return Response(spot_api(request))

@api_view(['GET', 'POST'])
def get_prd(request):
    prd_json = api_call(request)
    # print(prd_json)
    # c1ard_list, jwt_token = my_data_cleaner(card_list)
    # for card in card_list:
    #     card_approval = get_card_approval(jwt_token, card['card_id'])
    # prd_json이 이미 dict라면
    return Response(prd_json)

