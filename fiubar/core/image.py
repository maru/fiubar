# -*- coding: utf-8 -*-
from StringIO import StringIO

from django.utils.translation import ugettext as _
from PIL import Image


def rescale_upload(photo, size, path=None, quality=100, format='jpeg', canvas=None):
	"""Function is used"""
	return rescale(StringIO(photo), size, path, quality, format, canvas)

def rescale(photo, size, path=None, quality=100, format='jpeg', canvas=None):
	"""Function is used"""
	image = Image.open(photo)
	# needed to save GIF format to jpeg
	image = image.convert("RGB")

	if format.lower() == 'jpg':
		format = 'jpeg'

	if canvas == 'box':
		image = crop_box(image)
	elif canvas == 'rel':
		image = crop_relative(image, size)

	# Resize if bigger
	image.thumbnail(size, Image.ANTIALIAS)

	# Save the image
	image.save(path, format, quality=quality)

	if isinstance(path, StringIO):
		return path.getvalue()
	return image

def crop_box(image):
	"""Function is used"""
	width, height = image.size
	if width > height:
		left  = (width - height) / 2
		upper = 0
		right = (width + height) /2
		lower = height
	else: # if width <= height:
		left  = 0
		upper = (height - width) / 2
		right = width
		lower = (height + width) / 2

	bounds = (left, upper, right, lower)
	newimage = image.crop(bounds)
	return newimage

def crop_relative(image, size):
	"""Crop image relative to the size"""
	width, height = image.size
	new_width, new_height = size
	
	factor_w = width/(new_width*1.0)
	factor_h = height/(new_height*1.0)
	h = int(round(height/factor_w))

	if h == new_height:
		left = 0
		upper = 0
		right = width
		lower = height
	elif h > new_height:
		left  = 0
		upper = int(round((height - new_height*factor_w) / 2))
		right = width
		lower = int(round(upper + new_height*factor_w))
	elif h < new_height:		
		left  = int(round((width - new_width*factor_h) / 2))
		upper = 0
		right = int(round(left + new_width*factor_h))
		lower = height

	bounds = (left, upper, right, lower)
	newimage = image.crop(bounds)
	return newimage
