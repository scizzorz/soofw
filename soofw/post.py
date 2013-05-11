import os, re, time # python
import markdown2 # dependencies
from soofw import toc # local

# get the path to the content directory
APP_ROOT = os.path.dirname(os.path.realpath(__file__))
CONTENT_ROOT = os.path.join(APP_ROOT, 'content')

RE_MODE = re.compile(r'^\[(\w+)\]$')
RE_META = re.compile(r'^\* (\w+)\s*=\s*(.*)$')
RE_HEADER = re.compile(r'^\#+.*$')
RE_RULE = re.compile(r'^[\-\~]{3,}$')

FMT_DATETIME = '%m/%d/%Y %I:%M%p'

# raised when a post couldn't be opened
class PostNotFoundError(Exception):
	def __init__(self, path):
		self._path = path
		Exception.__init__(self)

	def __str__(self):
		return 'Unable to open post "%s".' % self._path

# used to load and process a post
class Post:
	def __init__(self, path, mode = 'preview'):
		self._metas = dict()
		self._source = ''

		self.timestamp = 0
		self.add_continue = False
		self.path = os.path.basename(os.path.dirname(path))
		self.basename = os.path.basename(path)

		self._mode = mode
		self._load(path)

	# load the file and then pass it to the parser / processor
	def _load(self, path):
		try:
			sourcefile = open(path, 'r+')
		except IOError:
			raise PostNotFoundError(path)
		else:
			self._parse(sourcefile)
			self._process()

	# read the file and parse the metaprops and source code
	def _parse(self, sourcefile):
		metamode = 'meta'
		for line in sourcefile:
			if metamode == 'meta':
				temp = RE_META.match(line)
				if temp:
					# we are, so assign the metaprop
					# infer the type if possible
					if temp.group(2).lower() == 'true': # bool
						self[temp.group(1)] = True
					elif temp.group(2).lower() == 'false':
						self[temp.group(1)] = False

					elif temp.group(2).isdigit(): # int
						self[temp.group(1)] = int(temp.group(2))

					elif temp.group(1) == 'tags': # this one I *know* is a list, so we might as well convert it.
						self[temp.group(1)] = temp.group(2).split(' ')
						self[temp.group(1)].sort()

					else: # str
						self[temp.group(1)] = temp.group(2)
				else:
					metamode = self._mode

			# otherwise, just add the line to the source
			elif metamode == 'preview' or metamode == 'full':
				is_header = RE_HEADER.match(line)
				is_rule = RE_RULE.match(line)

				if metamode == 'preview' and (is_header or is_rule):
					self.add_continue = True
					return

				self._source += line

	# actually do things with the metaprops, like convert a datetime into a timestamp
	def _process(self):
		# check for a datetime
		if 'datetime' in self:
			timestamp = time.strptime(self['datetime'], FMT_DATETIME)
			self.timestamp = time.mktime(timestamp)

	# render the markdown (if necessary)
	def render(self):
		if self._mode == 'preview' or 'notoc' in self:
			return markdown2.markdown(self._source)
		else:
			return toc.toc(markdown2.markdown(self._source), 'nonum' in self)

	# rich sorting
	def __eq__(self, other):
		return self.timestamp == other.timestamp
	def __ne__(self, other):
		return self.timestamp != other.timestamp
	def __le__(self, other):
		return self.timestamp < other.timestamp
	def __lt__(self, other):
		return self.timestamp <= other.timestamp
	def __ge__(self, other):
		return self.timestamp > other.timestamp
	def __gt__(self, other):
		return self.timestamp >= other.timestamp

	# dict features
	def __len__(self):
		return len(self._metas)
	def __getitem__(self, key):
		return self._metas[key]
	def __setitem__(self, key, value):
		self._metas[key] = value
	def __delitem__(self, key):
		del self._metas[key]
	def __contains__(self, item):
		return item in self._metas

CACHE = dict()

# get all posts in a directory
def get_posts(path, mode = 'preview'):
	files = os.listdir(get_path(path))
	posts = []
	for name in files:
		posts.append(get_post(path, name, mode))

	posts.sort()

	return posts

# get a single post
def get_post(path, name, mode = 'preview'):
	full_path = get_path(path, name)
	# use the mode AND the full_path for the key
	# otherwise it caches things poorly
	key = mode + '@' + full_path

	if full_path not in CACHE:
		CACHE[key] = Post(full_path, mode)

	return CACHE[key]

# get the full path to content
def get_path(*args):
	return os.path.join(CONTENT_ROOT, *args)
