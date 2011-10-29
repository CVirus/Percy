# -*- coding: utf-8 -*-

from Bayern.models import Piece
from django.http import HttpResponse

def index(request):
	result = 0
	for i in Piece.objects.all():
		result += (i.shop_stock + i.store_stock)*i.store_buying_price

	return HttpResponse(str(result) + "جنيه مصري ")

