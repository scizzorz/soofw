import re

HEADER = re.compile(r'<[hH](?P<level>\d)>(?P<text>.*)</[hH](?P=level)>')
SUB = re.compile(r'\s*<span.*sub.*>.*</span>\s*')
TAG = re.compile(r'</?.*?>')
BLANK = re.compile(r'[\'\"\.]')
HYPHEN = re.compile(r'[^a-z0-9\-]+')
END_HYPHENS = re.compile(r'(^\-)|(\-$)')

# replace any punctuation and crap characters with a hyphen
def prettify(string):
	string = string.lower()
	string = TAG.subn('', string)[0]
	string = BLANK.subn('', string)[0]
	string = HYPHEN.subn('-', string)[0]
	string = END_HYPHENS.subn('', string)[0]
	return string

def get_add_id(stack):
	def add_id(match):
		level = match.group('level')
		text = match.group('text')
		clean_text = text
		if SUB.search(clean_text):
			clean_text = SUB.sub('', clean_text)
		i = prettify(clean_text)

		stack.append((level, i, clean_text))
		return '<h%s id="%s">%s</h%s>' % (level, i, text, level)
	return add_id

def toc(html, nonum = False):
	# split the HTML into lines,
	# make a new list to store the processed HTML,
	# make a TOC stack,
	# and get the scoped add_id regex replace function
	html_lines = html.split('\n')
	new_lines = []
	stack = []
	add_id = get_add_id(stack)

	# loop through the lines, appending the modified line to our output list
	for line in html_lines:
		new_lines.append(HEADER.sub(add_id, line))

	contents = ''
	header_depth = 0
	list_depth = 0
	for link in stack:
		level = int(link[0])

		# if our level didn't change, we can close this immediately
		if level <= header_depth:
			contents += '</li>\n'


		# essentially, this is our first item in the stack
		if header_depth == 0:
			# so open with an id'd <ol> and increment list depth
			if nonum:
				contents += '<ol id="toc" class="nonum shaded-links">'
			else:
				contents += '<ol id="toc" class="shaded-links">\n'
			list_depth += 1

		#  we've indented more
		elif level > header_depth:
			# open a new <ol> and increment list depth
			contents += '\n<ol>\n'
			list_depth += 1

		# we're outdenting, so close any open <ol>
		elif level < header_depth:
			# header_depth - level is to ensure that if you jump from an h5
			# to an h2 it will close enough lists
			for _ in range(header_depth - level):
				contents += '</ol>\n'
				list_depth -= 1

			# then close the still open <li>
			contents += '</li>\n'

		# open a new <li> with the link
		contents += '<li><a href="#%s">%s</a>' % (link[1], link[2])

		# update the new header depth
		header_depth = level

	# close any remaining lists
	while list_depth > 0:
		if list_depth == 1:
			contents += '</li>\n<li id="top"><a href="#container">back to top</a></li>\n</ol>\n'
		else:
			contents += '</li>\n</ol>\n'
		list_depth -= 1

	return ("\n".join(new_lines)) + contents
