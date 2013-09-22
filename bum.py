import bumpy, soofw

@bumpy.generates('*.pyc', 'soofw/*.pyc')
def clean():
	'Removes all generated files.'
	bumpy.clean()

@bumpy.method
@bumpy.requires('soofw/scss/main.scss', 'soofw/scss/_include.scss')
@bumpy.generates('soofw/static/main.css')
def css(self):
	'Compiles the SCSS into CSS.'

	# only build CSS if the SCSS is newer
	if bumpy.age(*self.requirements) < bumpy.age(self.generates[0]):
		import scss
		_scss = scss.Scss({}, {'compress': False, 'debug_info': False})

		main_file = open(self.generates[0], 'w')
		main_file.write(_scss.compile(scss_file=self.requirements[0]))

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
