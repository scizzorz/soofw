all: css links

clean:
	rm -rf soofw/static/*.css soofw/*.pyc soofw/content/links.md

# all CSS stuff
css: soofw/static/main.css

soofw/static/main.css: soofw/scss/main.scss soofw/scss/_include.scss
	pyscss -C soofw/scss/main.scss > soofw/static/main.css


links: soofw/content/links.md

# I want this to also depend on my delicious profile, c'est la vie.
soofw/content/links.md: fetch_delicious.py
	python fetch_delicious.py
