from urlparse import urlparse
import deliciousapi

API = deliciousapi.DeliciousAPI()
USER = API.get_user('scizzorz')

URL = 0
TAGS = 1
TITLE = 2
COMMENT = 3
TIMESTAMP = 4

def main():
	bundle = {}
	tags = []

	for bookmark in USER.bookmarks:
		for tag in bookmark[TAGS]:
			if not tag.strip(): # don't add blank tags
				continue

			if not tag in tags: # add this tag to the tag list
				tags.append(tag)

			if not tag in bundle: # add this tag to the tag bundle
				bundle[tag] = []

			bundle[tag].append(bookmark) # add this link to the bundle

	# sort the tags
	tags.sort()

	# open the file and write our intro paragraph
	# figure out a better way to make this intro paragraph, man
	filed = open('soofw/content/links.md', 'w')
	filed.write("""* title = Links
* page_title = links
* navkey = links
* nonum = True

Here are some links I found and thought were pretty cool. They're grouped by tag, so some links will occur more than one time. The list can also be found on my [Delicious profile](https://delicious.com/scizzorz).

""")

	for tag in tags:
		print "%s x%d" % (tag, len(bundle[tag]))
		filed.write("### %s\n\n" % tag)

		for bookmark in bundle[tag]:
			parts = urlparse(bookmark[URL])
			base_url = parts.netloc
			if base_url[0:4] == 'www.':
				base_url = base_url[4:]

			#print "\t%s @ %s" % (bookmark[TITLE], base_url)
			format_tuple = (bookmark[TITLE], bookmark[URL], base_url)
			filed.write('* [**%s**](%s) <span class="subtle">%s</span>\n\n' % format_tuple)
			if bookmark[COMMENT]:
				filed.write("  %s\n\n" % bookmark[COMMENT])

if __name__ == '__main__':
	main()
