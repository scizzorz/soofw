#!/usr/bin/env python
import soofw
from bumpy import *

@task
def clean():
	'Removes all generated files.'
	shell('rm -rf soofw/static/*.css')
	shell('rm -rf *.pyc')
	shell('rm -rf soofw/*.pyc')
	shell('rm -rf soofw/content/links.md')

@requires('soofw/scss/main.scss', 'soofw/scss/_include.scss')
def css():
	'Compiles the SCSS into CSS.'

	# only build CSS if the SCSS is newer
	if age('soofw/scss/main.scss', 'soofw/scss/_include.scss') < age('soofw/static/main.css'):
		import scss
		_scss = scss.Scss({}, {'compress': False, 'debug_info': False})

		main_file = open('soofw/static/main.css', 'w')
		main_file.write(_scss.compile(scss_file = 'soofw/scss/main.scss'))

@task
def links():
	'Generates the "links" page.'
	import fetch_delicious
	fetch_delicious.main()

@default
@requires(css, links)
def all():
	'Generates all necessary files.'
	pass

@task
def run():
	'Runs the server.'
	soofw.app.run(host='0.0.0.0', debug=True)