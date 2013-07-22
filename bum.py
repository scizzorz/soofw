import bumpy, soofw

@bumpy.task
def clean():
	'Removes all generated files.'
	bumpy.shell('rm -rf *.pyc soofw/*.pyc')
	bumpy.clean()

@bumpy.requires('soofw/scss/main.scss', 'soofw/scss/_include.scss')
@bumpy.generates('soofw/static/main.css')
def css():
	'Compiles the SCSS into CSS.'

	# only build CSS if the SCSS is newer
	if bumpy.age('soofw/scss/main.scss', 'soofw/scss/_include.scss') < bumpy.age('soofw/static/main.css'):
		import scss
		_scss = scss.Scss({}, {'compress': False, 'debug_info': False})

		main_file = open('soofw/static/main.css', 'w')
		main_file.write(_scss.compile(scss_file = 'soofw/scss/main.scss'))

@bumpy.generates('soofw/content/links.md')
def links():
	'Generates the "links" page.'
	import fetch_delicious
	fetch_delicious.main()

@bumpy.default
@bumpy.requires(css, links)
def all():
	'Generates all necessary files.'
	pass

@bumpy.task
def run():
	'Runs the server.'
	soofw.app.run(host='0.0.0.0', debug=True)
