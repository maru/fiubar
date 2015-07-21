from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.conf import settings
from openmate.core.log import logger
import md5, os, errno

class StaticDirSystemStorage(FileSystemStorage):
	"""
	Static directory filesystem storage
	"""

	def __init__(self, location=settings.STATIC_ROOT, base_url=settings.STATIC_URL):
		location = settings.STATIC_ROOT
		base_url = settings.STATIC_URL
		super(StaticDirSystemStorage, self).__init__(location, base_url)


	def _save(self, name, content):
		return super(StaticDirSystemStorage, self)._save(name, content)

class MD5SystemStorage(StaticDirSystemStorage):
	"""
	MD5 file name based filesystem storage
	"""

	def _save(self, name, content):
		# Get md5 sum of file
		content.open()
		file_name = md5.new(content.read()).hexdigest()

		# name is `upload_to dir`/filename.ext
		directory = os.path.dirname(name)
		file_ext = name.split('.')[-1]
		name = u'%s/%s.%s' % (directory, file_name, file_ext)

		if self.exists(name):
			logger.error('0.0.0.0 - md5 collision! %s exists.' % name)

		return super(MD5SystemStorage, self)._save(name, content)

class RescaleImageSystemStorage(StaticDirSystemStorage):
	"""
	Rescale image filesystem storage
	"""

	def __init__(self, location=settings.STATIC_ROOT, base_url=settings.STATIC_URL, width=140, height=140, canvas=None):
		self.width = width
		self.height = height
		self.canvas = canvas
		super(RescaleImageSystemStorage, self).__init__(location, base_url)

	def _save(self, name, content):
		print name
		from openmate.core.image import rescale
		from StringIO import StringIO
		stream = StringIO()
		file_ext = name.split('.')[-1]
		f = rescale(content, [self.width, self.height], canvas=self.canvas, format=file_ext, path=stream)
		return super(RescaleImageSystemStorage, self)._save(name, ContentFile(f))
