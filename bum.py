import sys, bumpy as b
if '.' not in sys.path: sys.path.append('.')
import soofw

@b.generates('*.pyc **/*.pyc')
def clean():
	'''Remove all generated files.'''

	b.clean()

@b.method
@b.requires('soofw/scss/main.scss', 'soofw/scss/_include.scss')
@b.generates('soofw/static/main.css')
def css(self):
	'''Compile the SCSS into CSS.'''

	# only build CSS if the SCSS is newer
	if b.age(*self.file_requirements) < b.age(self.generates):
		import scss
		_scss = scss.Scss({}, {'compress': False, 'debug_info': False})

		main_file = open(self.generates, 'w')
		main_file.write(_scss.compile(scss_file=self.file_requirements[0]))

@b.generates('soofw/content/links.yml')
def links():
	'''Generate the "links" page.'''

	import fetch_delicious
	fetch_delicious.main()

@b.default
@b.requires(css, links)
def all():
	'''Generate all necessary files.'''

	pass

@b.task
def run():
	'''Run the server.'''

	soofw.app.run(host='0.0.0.0', debug=True)
