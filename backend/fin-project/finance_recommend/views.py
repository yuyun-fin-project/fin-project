from .utils.spot.spot_api import spot_api
from rest_framework.response import Response

# Create your views here.
def get_spot(request):
    return Response(spot_api(request))