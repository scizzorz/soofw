from datetime import datetime as dt
from werkzeug import routing
from soofw import app # local

# format a date for web
@app.template_filter('date')
def format_date(article):
	# if there's no datetime, just return blank...
	if 'datetime' not in article:
		return ''

	delta = dt.today() - article['datetime']

	# today: just the time
	if delta.days == 0:
		return article['datetime'].strftime('today at %l:%M%p')

	formatted = article['datetime'].strftime('%B %e')

	# add ordinal suffix
	if formatted[-2:] in ('11', '12', '13'):
		formatted += 'th'
	elif formatted[-1:] in ('0', '4', '5', '6', '7', '8', '9'):
		formatted += 'th'
	elif formatted[-1:] == '1':
		formatted += 'st'
	elif formatted[-1:] == '2':
		formatted += 'nd'
	elif formatted[-1:] == '3':
		formatted += 'rd'

	# last year: add the year
	if dt.today().year != article['datetime'].year:
		formatted += article['datetime'].strftime(', %Y')

	return formatted

@app.template_filter('date_short')
def format_date_short(article):
	if 'datetime' not in article:
		return ''

	return article['datetime'].strftime('%b %Y')

# format the date for the RSS feed
@app.template_filter('date_rss')
def format_date_rss(article):
	if 'datetime' not in article:
		return ''

	return article['datetime'].strftime('%a, %d %B %Y %H:%M:%S %Z')

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
