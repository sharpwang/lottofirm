from sgmllib import SGMLParser
import htmlentitydefs
import urllib2
import re
import mysql.connector

class BaseStripper(object):
	def __init__(self, sgmlparser):
		self.sgmlparser = sgmlparser

	def process_data(self, text):
		self.sgmlparser.pieces.append(text)

	def process_tag(self, text):
		self.sgmlparser.pieces.append("<%s>" % text)


class BaseHTMLProcessor(SGMLParser):
	def reset(self):
		self.pieces = []
		self.stripper = BaseStripper(self)
		self.skipscript = False
		SGMLParser.reset(self)

	def unknown_starttag(self, tag, attrs):
		self.stripper.process_tag(tag)

	def unknown_endtag(self, tag):
		#self.pieces.append("</%(tag)s>" % locals())
		pass
	
	def handle_data(self, text):
		if self.skipscript:
			pass
		else:
			self.stripper.process_data(text)

	def start_script(self, text):
		self.skipscript = True

	def end_script(self):
		self.skipscript = False
	
	def output(self):
	
		extract = "".join(self.pieces)

		print extract
		m = re.search("<table>([^<]+)<tr>\s+<td>\s+<span><a>([^<]+)<font><strong>([^<]+)<span>([^<]+)<tr>", extract)
		print m.group(1), m.group(2), m.group(3), m.group(4)

		m = re.search("<td>([^<]+)<td>\s+<div>\s+<ul>\s+<li>(\d{2})[^<]+<li>(\d{2})[^<]+<li>(\d{2})[^<]+<li>(\d{2})[^<]+<li>(\d{2})[^<]+<li>(\d{2})[^<]+<li>(\d{2})", extract)
		print m.group(1), m.group(2), m.group(3),m.group(4), m.group(5), m.group(6),m.group(7), m.group(8)

		m = re.search("<li>\d{2}\s+<tr>[^<]+<td>([^<]+)<td>([^<]+)", extract)
		print m.group(1), m.group(2)

		m = re.search("<tr>[^<]+<td>([^<]+)<span>([^<]+)<span>([^<]+)", extract)
		print m.group(1), m.group(2), m.group(3)


		p = re.compile("<tr>[^<]+<td>([^<]+)<td>([^<]+)<td>([^<]+)<td>([^<]+)\s+<tr>[^<]+<td>([^<]+)<td>([^<]+)<td>([^<]+)")
		m = p.search(extract, 1)
		print m.group(1), m.group(2), m.group(3),m.group(4), m.group(5), m.group(6), m.group(7)
		m = p.search(extract, m.end())
		print m.group(1), m.group(2), m.group(3),m.group(4), m.group(5), m.group(6), m.group(7)
		m = p.search(extract, m.end())
		print m.group(1), m.group(2), m.group(3),m.group(4), m.group(5), m.group(6), m.group(7)
		m = p.search(extract, m.end())


response= urllib2.urlopen('http://kaijiang.500.com/dlt.shtml', timeout=10)
html = response.read().decode('gbk').encode('utf-8')
#print repr(html)
response.close()
parser = BaseHTMLProcessor()
parser.feed(html)
parser.output()
parser.close()

conn = mysql.connector.connect(host='lottofirm.net', user='root', password='wang3', database='lottofirm', use_unicode=True)
cursor = conn.cursor()
n = cursor.execute('select * from CZBM')
print n
results = cursor.fetchall()
for r in results:
	print r
print n