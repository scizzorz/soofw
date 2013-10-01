import time # python
from werkzeug import routing
from soofw import app # local

# format a date for web
@app.template_filter('date')
def format_date(article):
	return 'FIXME'

	# if there's no timestamp, just return blank...
	if article.timestamp == 0:
		return ''

	# make the time_structs
	time_struct = time.localtime(article.timestamp)
	cur_time_struct = time.localtime()

	# default: just the month and day
	date_fmt = '%B %e'
	add_ord_suffix = True
	prefix = ""

	# today: just the time
	if time_struct.tm_yday == cur_time_struct.tm_yday:
		date_fmt = '%I:%M%p'
		add_ord_suffix = False
		prefix = 'today at '

	formatted = time.strftime(date_fmt, time_struct)

	# add an ordinal suffix
	if add_ord_suffix:
		# these are dumb
		if formatted[-2:] in ('11', '12', '13'):
			formatted += 'th'

		# these are average
		elif formatted[-1:] in ('0', '4', '5', '6', '7', '8', '9'):
			formatted += 'th'

		# the rest are dumb
		elif formatted[-1:] == '1':
			formatted += 'st'
		elif formatted[-1:] == '2':
			formatted += 'nd'
		elif formatted[-1:] == '3':
			formatted += 'rd'

	# last year: add the year
	if time_struct.tm_year != cur_time_struct.tm_year:
		formatted += time.strftime(', %Y', time_struct)

	# strip the leading zero from the formatted text
	# only useful for the time part
	if formatted[0] == '0':
		formatted = formatted[1:]


	return prefix + formatted

@app.template_filter('date_prep')
def format_date_prep(article):
	return 'FIXME'

	# if there's no timestamp, just return blank...
	if article.timestamp == 0:
		return ''

	# make the time_structs
	time_struct = time.localtime(article.timestamp)
	cur_time_struct = time.localtime()

	# last year: "on" may 27th, 2012
	if time_struct.tm_year != cur_time_struct.tm_year:
		return 'on'

	# today: "" today at 7:30pm
	if time_struct.tm_yday == cur_time_struct.tm_yday:
		return ''

	# default: "on" may 27th
	return 'on'

@app.template_filter('date_short')
def format_date_short(article):
	date_fmt = '%b %Y'

	time_struct = time.localtime(article.timestamp)

	return time.strftime(date_fmt, time_struct)


# format the date for the RSS feed
@app.template_filter('date_rss')
def format_date_rss(article):
	return 'FIXME'
	time_struct = time.localtime(article.timestamp)
	return time.strftime('%a, %d %B %Y %H:%M:%S %Z', time_struct)

# only accept certain paths for blog-style areas
class BlogConverter(routing.BaseConverter):
	def __init__(self, map):
		super(BlogConverter, self).__init__(map)
		self.regex = r'\w+'

	def to_python(self, value):
		if value in ('thoughts',):
			return value

		raise routing.ValidationError()

	def to_url(self, value):
		return value

# only accept certain paths for page-style areas
class PageConverter(routing.BaseConverter):
	def __init__(self, map):
		super(PageConverter, self).__init__(map)
		self.regex = r'\w+'

	def to_python(self, value):
		if value in ('links', 'projects', 'demos'):
			return value

		raise routing.ValidationError()

	def to_url(self, value):
		return value

app.url_map.converters['blog'] = BlogConverter
app.url_map.converters['page'] = PageConverter
