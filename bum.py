import bumpy as b
import sys
import soofw

@b.task(gens='*.pyc **/*.pyc')
def clean():
	'''Remove all generated files'''
	b.clean()

@b.task('method', reqs=('soofw/scss/main.scss', 'soofw/scss/_include.scss'), gens='soofw/static/main.css')
def css(self):
	'''Compile the SCSS into CSS'''
	# only build CSS if the SCSS is newer
	if b.age(*self.file_reqs) < b.age(self.gens):
		import scss
		_scss = scss.Scss({}, {'compress': False, 'debug_info': False})

		main_file = open(self.gens, 'w')
		main_file.write(_scss.compile(scss_file=self.file_reqs[0]))

@b.task('default', reqs=css)
def all():
	'''Generate all necessary files'''
	pass

@b.task
def run():
	'''Run the server'''
	soofw.app.run(host='0.0.0.0', debug=True)
