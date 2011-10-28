# -*- coding: utf-8 -*-

from Bayern.models import Piece, StoreTransaction, ShopTransaction
from django.contrib import admin
from django import forms


class PieceAdmin(admin.ModelAdmin):
	list_per_page = 200
	fieldsets = [(None, {'fields': ['name', 'serial','st', 'description', 'barcode']}), ('المتجر', {'fields': ['shop_stock', 'shop_min_stock', 'shop_selling_price', 'shop_place']}), ('المخزن', {'fields': ['store_stock', 'store_min_stock', 'store_buying_price', 'store_place']})]
	list_display = ('id', 'formatted_serial', 'name', 'colored_shop_stock', 'colored_store_stock', 'st', 'description', 'shop_place_ltr', 'shop_selling_price')
	ordering = ['id']
	search_fields = ['id', 'name', 'serial', 'description']
	list_filter = ['st']
	list_display_links = ('formatted_serial',)


	class Media:
		css = {
			"all": ("my_styles.css",)
			}


class StoreTransactionAdmin(admin.ModelAdmin):
	fields = ('date','piece_name', 'piece_place', 'piece', 'transaction_type', 'number_of_pieces', 'notes', 'price')
	readonly_fields = ('piece_name', 'piece_place', 'price')
	list_display = ('date', 'piece_serial', 'piece_name', 'piece_place', 'transaction_type', 'number_of_pieces', 'notes', 'store_stock', 'price', 'piece_st')
	list_filter = ['date', 'transaction_type']
	date_hierarchy = 'date'
	search_fields = ['piece__name', 'piece__serial', 'price', 'piece__store_place']
	raw_id_fields = ("piece",)


	class Media:
		css = {
			"all": ("my_styles.css",)
			}


class ShopTransactionAdmin(admin.ModelAdmin):
	radio_fields = {"transaction_type": admin.VERTICAL}
	fields = ('date','piece_name', 'piece_place', 'piece', 'transaction_type', 'number_of_pieces', 'notes', 'piece_price', 'price')
	readonly_fields = ('piece_name', 'piece_place', 'price')
	list_display = ('date', 'piece_serial', 'piece_name', 'piece_place', 'transaction_type', 'number_of_pieces', 'notes', 'shop_stock', 'piece_price', 'price', 'piece_st')
	list_filter = ['date', 'transaction_type']
	date_hierarchy = 'date'
	search_fields = ['piece__name', 'piece__serial', 'price', 'piece__shop_place']
	raw_id_fields = ("piece",)


	class Media:
		css = {
			"all": ("my_styles.css",)
			}


admin.site.register(Piece, PieceAdmin)
admin.site.register(StoreTransaction, StoreTransactionAdmin)
admin.site.register(ShopTransaction, ShopTransactionAdmin)
