import flask, os, yaml
from soofw import app

POSTS_PER_PAGE = 6
app.config['NAVIGATION'] = ['thoughts', 'projects', 'demos', 'links']

# view a list of posts
@app.route('/<blog:post_path>/')
@app.route('/<blog:post_path>/<int:page>/')
@app.route('/<blog:post_path>/tag/<tag>/')
@app.route('/<blog:post_path>/tag/<tag>/<int:page>/')
def view_list(post_path, tag = None, page = 1):
	articles = [yaml.load(open(path)) for path in os.listdir('soofw/content/' + post_path)]

	# make them reverse chronological order
	articles.reverse()

	# grab the tagged articles if we need to
	if tag:
		articles = [article for article in articles
			if ('tags' in article and tag in article['tags'])]

	# drop the page by one to dehumanize it
	page -= 1

	# don't go past the page limit!
	if POSTS_PER_PAGE * page >= len(articles) or page < 0:
		return flask.redirect('/'+post_path)

	# figure out the number of pages and the min/max of our current page
	pages = len(articles) / POSTS_PER_PAGE + 1
	min_post = POSTS_PER_PAGE * page
	max_post = min(min_post + POSTS_PER_PAGE, len(articles))

	# set the navkey based on the current page
	if not page:
		flask.g.navkey = post_path

	return flask.render_template('main-list.html',
		title = post_path,
		articles = articles[min_post:max_post],
		pages = pages,
		page = page,
		tag = tag,
		path = post_path)

# view a tag-sorted list of post titles
@app.route('/<blog:post_path>/archive/')
def view_archive(post_path):
	# open all the articles as previews
	articles = [yaml.load(open(path)) for path in os.listdir('soofw/content/' + post_path)]

	# make them reverse chronological order
	articles.reverse()

	bundle = {}
	tags = []
	for article in articles:
		if 'tags' in article:
			for tag in article['tags']:
				if tag not in tags:
					tags.append(tag)

				if tag not in bundle:
					bundle[tag] = []

				bundle[tag].append(article)

	return flask.render_template('main-archive.html',
		bundle = bundle,
		tags = sorted(tags),
		path = post_path)

# view an RSS feed
@app.route('/<blog:post_path>/rss.xml')
def view_rss(post_path):
	# open all the articles as full posts
	articles = [yaml.load(open(path)) for path in os.listdir('soofw/content/' + post_path)]

	# make them reverse chronological order
	articles.reverse()

	# get at most 10 articles
	max_post = min(10, len(articles))

	# we need to add a text/xml header, so we need a new response object
	response = flask.make_response(flask.render_template('main-rss.html',
		title = 'soofw / {}'.format(post_path),
		articles = articles[:max_post],
		link = 'http://soofw.com/' + post_path,
		desc = "A collection of my {}".format(post_path)))
	response.headers['Content-Type'] = 'text/xml'
	return response

# view a single post
@app.route('/post/<int:post_name>/', defaults = {'post_path':'legacy'})
@app.route('/<blog:post_path>/<post_name>/')
def view_single(post_path, post_name):
	# open the article
	article = yaml.load(open('soofw/content/' + post_path + '/' + str(post_name) + '.yml'))

	# if it has a meta redirect, follow it
	if 'redirect' in article:
		return flask.redirect(article['redirect'], 301)

	return flask.render_template('main-single.html',
		article = article)

# view a page
@app.route('/', defaults = {'post_name':'home'})
@app.route('/<page:post_name>/')
def view_page(post_name, post_path = ''):
	# open the article
	article = yaml.load(open('soofw/content/' + post_path + '/' + str(post_name) + '.yml'))

	flask.g.navkey = article['navkey']

	return flask.render_template('main-page.html', article = article)

# old paging URI
@app.route('/<int:page>/')
def legacy_paging(page):
	return flask.redirect('/thoughts/{}/'.format(page), 301)

# old post URI
@app.route('/post/<post_id>/')
def legacy_post(post_id):
	return flask.redirect('/thoughts/{}/'.format(post_id), 301)

# error handling, derp
@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(500)
def view_error(error):
	# try displaying it like an HTTPException
	try:
		return flask.render_template('error.html',
			error = '{} Error'.format(error.code),
			desc = error.description), error.code

	# guess not.
	except:
		return flask.render_template('error.html',
			error = 'Oh noes',
			desc = 'No description available.')
