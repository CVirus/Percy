# -*- coding: utf-8 -*-

import datetime
from django.db import models


class Piece(models.Model):
	name = models.CharField(verbose_name='إسم القطعة', max_length=200)
	serial = models.CharField(verbose_name='الرقم التسلسلي', unique=False, max_length=11)
	description = models.TextField(verbose_name='الوصف', null=True, blank=True)
	st = models.BooleanField(verbose_name='أصلي')
	barcode = models.DecimalField(verbose_name='بار كود', null=True, blank=True, max_digits=20, decimal_places=0)

	shop_stock = models.PositiveIntegerField(verbose_name='رصيد')
	shop_min_stock = models.PositiveIntegerField(verbose_name='الحد الأدني')
	shop_min_stock_reached = models.BooleanField(default=False)
	shop_selling_price = models.PositiveIntegerField(verbose_name='سعر البيع')
	shop_place = models.CharField(verbose_name='المكان', max_length=200)

	store_stock = models.PositiveIntegerField(verbose_name='رصيد')
	store_min_stock = models.PositiveIntegerField(verbose_name='الحد الأدني')
	store_min_stock_reached = models.BooleanField(default=False)
	store_buying_price = models.PositiveIntegerField(verbose_name='سعر الشراء')
	store_place = models.CharField(verbose_name='المكان', max_length=200)

	def __unicode__(self):
		return str(self.serial)

	def formatted_serial(self):
		if len(str(self.serial)) == 11:
			if self.st == True:
				return '<span style="color:green" dir="ltr">%s</span>' % (insert(insert(insert(insert(str(self.serial), ' ', 2), ' ', 5), ' ', 7), ' ', 11))
			else:
				return '<span style="color:red" dir="ltr">%s</span>' % (insert(insert(insert(insert(str(self.serial), ' ', 2), ' ', 5), ' ', 7), ' ', 11))
		else:
			if self.st == True:
				return '<span style="color:green" dir="ltr">%s</span>' % (str(self.serial))
			else:
				return '<span style="color:red" dir="ltr">%s</span>' % (str(self.serial))

	formatted_serial.short_description = 'الرقم التسلسلي'
	formatted_serial.admin_order_field = 'serial'
	formatted_serial.allow_tags = True
	

	def is_shop_running_out(self):
		return self.shop_stock <= self.shop_min_stock

	def colored_shop_stock(self):
		if self.is_shop_running_out():
			return '<span style="color: red;">%s</span>' % (self.shop_stock)
		else:
			return self.shop_stock
	colored_shop_stock.allow_tags = True
	colored_shop_stock.admin_order_field = 'shop_stock'
	colored_shop_stock.short_description = 'رصيد المتجر'

	def shop_place_ltr(self):
		return '<span dir=ltr>%s</span>' % (self.shop_place)
	shop_place_ltr.allow_tags = True
	shop_place_ltr.admin_order_field = 'shop_place'
	shop_place_ltr.short_description = 'المكان'

	def store_place_ltr(self):
		return '<span dir=ltr>%s</span>' % (self.store_place)
	store_place_ltr.allow_tags = True
	store_place_ltr.admin_order_field = 'store_place'
	store_place_ltr.short_description = 'المكان'

	def is_store_running_out(self):
		return self.store_stock <= self.store_min_stock

	def colored_store_stock(self):
		if self.is_store_running_out():
			return '<span style="color: red;">%s</span>' % (self.store_stock)
		else:
			return self.store_stock
	colored_store_stock.allow_tags = True
	colored_store_stock.admin_order_field = 'store_stock'
	colored_store_stock.short_description = 'رصيد المخزن'

	class Meta:
			verbose_name = 'قطعة'
			verbose_name_plural = 'قطع'


def insert(original, new, pos):
	'''Inserts new inside original at pos.'''
	return original[:pos] + new + original[pos:]


class StoreTransaction(models.Model):
	TRANSACTION_TYPES = (('En', 'دخول'), ('Ex', 'خروج'),)
	piece = models.ForeignKey(Piece, verbose_name='رقم القطعة التسلسلي')
	date = models.DateTimeField(verbose_name='تاريخ')
	transaction_type = models.CharField(max_length='2', choices=TRANSACTION_TYPES, verbose_name='دخول/خروج', default='En')
	number_of_pieces = models.PositiveIntegerField(verbose_name='عدد القطع', default=1)
	#entry = models.PositiveIntegerField(verbose_name='دخول', default=0)
	#exit = models.PositiveIntegerField(verbose_name='خروج', default=0)
	notes = models.TextField(verbose_name='ملاحظات', max_length=200, blank=True)
	piece_price = models.BigIntegerField(verbose_name='سعر القطعة', editable=True, null=False, default=0)
	price = models.BigIntegerField(verbose_name='تكلفة المعاملة', editable=False, null=True)


	def __unicode__(self):
		return self.piece.name

	def piece_name(self):
		return self.piece.name
	piece_name.allow_tags = True
	piece_name.admin_order_field = 'piece__name'
	piece_name.short_description = 'إسم القطعة'

	def piece_serial(self):
		#return "<a href='Bayern%s'>%s</a>" % (self.piece.id, self.piece.formatted_serial())
		return self.piece.formatted_serial()
	piece_serial.allow_tags = True
	piece_serial.admin_order_field = 'piece__serial'
	piece_serial.short_description = 'رقم القطعة التسلسلي'

	def store_stock(self):
		return self.piece.colored_store_stock()
	store_stock.allow_tags = True
	store_stock.admin_order_field = 'piece__store_stock'
	store_stock.short_description = 'رصيد'

	def piece_place(self):
		return self.piece.store_place_ltr()
	piece_place.allow_tags = True
	piece_place.admin_order_field = 'piece__store_place'
	piece_place.short_description = 'مكان'

	def piece_st(self):
		if self.piece.st == False:
			return """<img alt="False" src="/static/admin/img/admin/icon-no.gif">"""
		else:
			return """<img alt="False" src="/static/admin/img/admin/icon-yes.gif">"""
	piece_st.allow_tags = True
	piece_st.admin_order_field = 'piece__st'
	piece_st.short_description = 'أصلي'


	def clean(self):
		from django.core.exceptions import ValidationError
		if self.transaction_type == 'Ex':
			if self.piece.store_stock < self.number_of_pieces:
				raise ValidationError('عدد قطع المخزن غير كافية')

	
	def save(self, *args, **kwargs):
		if self.transaction_type == 'En':
			print "will calc"
			self.piece.store_stock = self.piece.store_stock + self.number_of_pieces
			self.price = (self.number_of_pieces*self.piece_price).__neg__()
			self.piece.save()
		else:
			self.piece.store_stock = self.piece.store_stock - self.number_of_pieces
			shop_transaction = ShopTransaction(piece=self.piece,
												date=self.date,
												transaction_type='En',
												number_of_pieces=self.number_of_pieces,
												from_store=True,
												piece_price=0)
			shop_transaction.save()
		super(StoreTransaction, self).save(*args, **kwargs)

	class Meta:
			verbose_name = 'معاملة مخزن'
			verbose_name_plural = 'معاملات مخزن'


class ShopTransaction(models.Model):
	TRANSACTION_TYPES = (('En', 'دخول'), ('Ex', 'بيع'), ('Re', 'مرتجع'),)
	piece = models.ForeignKey(Piece, verbose_name='رقم القطعة التسلسلي')
	date = models.DateTimeField(verbose_name='تاريخ')
	transaction_type = models.CharField(max_length='2', choices=TRANSACTION_TYPES, verbose_name='نوع المعاملة')
	number_of_pieces = models.PositiveIntegerField(verbose_name='عدد القطع', default=1)
	notes = models.TextField(verbose_name='ملاحظات', max_length=200, blank=True)
	price = models.BigIntegerField(verbose_name='تكلفة المعاملة', editable=False, null=True)
	piece_price = models.BigIntegerField(verbose_name='سعر القطعة', null=False)
	from_store = models.BooleanField(default=False)

	def __unicode__(self):
		return self.piece.name

	def piece_name(self):
		return self.piece.name
	piece_name.allow_tags = True
	piece_name.admin_order_field = 'piece__name'
	piece_name.short_description = 'إسم القطعة'

	def piece_serial(self):
		#return "<a href='Bayern%s'>%s</a>" % (self.piece.id, self.piece.formatted_serial())
		return self.piece.formatted_serial()
	piece_serial.allow_tags = True
	piece_serial.admin_order_field = 'piece__serial'
	piece_serial.short_description = 'رقم القطعة التسلسلي'

	def shop_stock(self):
		return self.piece.colored_shop_stock()
	shop_stock.allow_tags = True
	shop_stock.admin_order_field = 'piece__shop_stock'
	shop_stock.short_description = 'رصيد'

	def piece_place(self):
		return self.piece.shop_place_ltr()
	piece_place.allow_tags = True
	piece_place.admin_order_field = 'piece__shop_place'
	piece_place.short_description = 'مكان'

	def piece_st(self):
		if self.piece.st == False:
			return """<img alt="False" src="/static/admin/img/admin/icon-no.gif">"""
		else:
			return """<img alt="False" src="/static/admin/img/admin/icon-yes.gif">"""
	piece_st.allow_tags = True
	piece_st.admin_order_field = 'piece__st'
	piece_st.short_description = 'أصلي'


	def clean(self):
		from django.core.exceptions import ValidationError
		if self.transaction_type == 'Ex':
			if self.piece.shop_stock < self.number_of_pieces:
				raise ValidationError('عدد قطع المتجر غير كافية')


	def save(self, *args, **kwargs):
		if self.transaction_type == 'En' or self.transaction_type == 'Re':
			print "will calc"
			self.piece.shop_stock = self.piece.shop_stock + self.number_of_pieces
			if self.from_store == False:
				self.price = (self.number_of_pieces*self.piece_price).__neg__()
		else:
			self.piece.shop_stock = self.piece.shop_stock - self.number_of_pieces
			self.price = (self.number_of_pieces*self.piece_price)
		self.piece.save()
		super(ShopTransaction, self).save(*args, **kwargs)

	class Meta:
			verbose_name = 'معاملة متجر'
			verbose_name_plural = 'معاملات متجر'
