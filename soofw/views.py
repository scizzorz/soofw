import flask # dependencies
from soofw import app, post # local

# navigation links
NAVIGATION =  ['thoughts', 'snippets', 'links', 'projects', 'demos']

# view a list of posts
@app.route('/thoughts/', defaults = {'post_path':'thoughts'})
@app.route('/thoughts/<int:page>/', defaults = {'post_path':'thoughts'})
@app.route('/thoughts/tag/<string:tag>/', defaults = {'post_path':'thoughts'})
@app.route('/thoughts/tag/<string:tag>/<int:page>/', defaults = {'post_path':'thoughts'})

@app.route('/snippets/', defaults = {'post_path':'snippets'})
@app.route('/snippets/<int:page>/', defaults = {'post_path':'snippets'})
@app.route('/snippets/tag/<string:tag>/', defaults = {'post_path':'snippets'})
@app.route('/snippets/tag/<string:tag>/<int:page>/', defaults = {'post_path':'snippets'})
def view_list(post_path, tag = None, page = 1, posts_per_page = 6):
	# open all the articles as previews
	try:
		articles = post.get_posts(post_path, mode = 'preview')
	except post.PostNotFoundError:
		flask.abort(404)
	else:
		# make them reverse chronological order
		articles.reverse()

		tags = []
		for article in articles:
			if 'tags' in article:
				for t in article['tags']:
					if t not in tags:
						tags.append(t)

		# grab the tagged articles if we need to
		if tag:
			articles = [article for article in articles if ('tags' in article and tag in article['tags'])]

	# drop the page by one to dehumanize it
	page -= 1

	# don't go past the page limit!
	if posts_per_page * page >= len(articles) or page < 0:
		return flask.redirect('/'+post_path)

	# figure out the number of pages and the min/max of our current page
	pages = len(articles) / posts_per_page + 1
	min_post = posts_per_page * page
	max_post = min(min_post + posts_per_page, len(articles))

	# set the page title and navkey based on the current page
	if page == 0:
		title = post_path
		navkey = post_path
	else:
		title = '%s (%d)' % (post_path, page + 1)
		navkey = None

	return flask.render_template('main-list.html',
			title = title,
			articles = articles[min_post:max_post],
			pages = pages,
			page = page,
			tag = tag,
			tags = sorted(tags),
			path = post_path,
			navkey = navkey,
			navigation = NAVIGATION)

# view an RSS feed
@app.route('/thoughts/rss.xml', defaults = {'post_path':'thoughts'})
@app.route('/snippets/rss.xml', defaults = {'post_path':'snippets'})
def view_rss(post_path):
	# open all the articles as full posts
	try:
		articles = post.get_posts(post_path, mode = 'full')
	except post.PostNotFoundError:
		flask.abort(404)
	else:
		# make them reverse chronological order
		articles.reverse()

	# get at most 10 articles
	max_post = min(10, len(articles))

	# we need to add a text/xml header, so we need a new response object
	response = flask.make_response(flask.render_template('main-rss.html',
		title = 'soofw / %s' % post_path,
		articles = articles[:max_post],
		link = 'http://soofw.com/' + post_path,
		desc = "A collection of my %s" % post_path))
	response.headers['Content-Type'] = 'text/xml'
	return response

# view a single post
@app.route('/post/<int:post_name>/', defaults = {'post_path':'legacy'})
@app.route('/thoughts/<string:post_name>/', defaults = {'post_path':'thoughts'})
@app.route('/snippets/<string:post_name>/', defaults = {'post_path':'snippets'})
def view_single(post_path, post_name):
	# open the article
	try:
		article = post.get_post(post_path, str(post_name)+'.md', mode = 'full')
	except post.PostNotFoundError:
		flask.abort(404)

	# if it has a meta redirect, follow it
	if 'redirect' in article:
		return flask.redirect(article['redirect'], 301)

	return flask.render_template('main-single.html',
			article = article,
			navigation = NAVIGATION)

# view a page
@app.route('/', defaults = {'post_path':'', 'post_name':'home'})
@app.route('/links/', defaults = {'post_path':'', 'post_name':'links'})
@app.route('/projects/', defaults = {'post_path':'', 'post_name':'projects'})
@app.route('/demos/', defaults = {'post_path':'', 'post_name':'demos'})
@app.route('/code/', defaults = {'post_path':'', 'post_name':'code'})
def view_page(post_path, post_name):
	# open the article
	try:
		article = post.get_post(post_path, post_name+'.md', mode = 'full')
	except post.PostNotFoundError:
		flask.abort(404)

	return flask.render_template('main-page.html',
			article = article,
			navkey = article['navkey'],
			navigation = NAVIGATION)

# old paging URI
@app.route('/<int:page>/')
def legacy_paging(page):
	return flask.redirect('/thoughts/%d/' % page, 301)

# old post URI
@app.route('/post/<string:post_id>/')
def legacy_post(post_id):
	return flask.redirect('/thoughts/%s/' % post_id, 301)

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
				error = '%d Error' % error.code,
				desc = error.description,
				navigation = NAVIGATION), error.code

	# guess not.
	except:
		return flask.render_template('error.html',
				error = 'Oh noes',
				desc = 'No description available.',
				navigation = NAVIGATION)
