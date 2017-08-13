from urllib import parse
import html
import requests
import re
from pprint import pprint

def urlize(m):
	s = m.group(1)
	if re.search('\|', s):
		page, name = s.split('|')
	else:
		name = s
		page = s
	page = page[0].upper() + page[1:]
	urlbase = 'https://wiki.factorio.com/'
	return '[{}]({})'.format(name, urlbase + 
		parse.quote_plus(re.sub(" ","_",page)))

def query(q):
	ret = ""
	if q == "":	
		return -1
	q = q[0].upper() + q[1:]
	querybase = 'https://wiki.factorio.com/api.php?action=query&titles='
	options = '&format=json&export&redirects'
	t = requests.get(querybase + parse.quote_plus(q) + options).json()
	if '-1' in t['query']['pages']:
		return -1
	page = t['query']['export']['*']
	#print (page)
	disambig = False
	for l in page.split('\n'):
		if re.search('\{\{disambiguation\}\}', l):
			disambig = True
			break
	
	start = False
	maxlines = 1
	lc = 0
	title = ""
	pstring = ""
	for l in page.split('\n'):
		t = re.search("\<title\>([^\<]*)", l)
		if t:
			title = t.group(1)
		if re.search("^['\[\w]", l) and not l.startswith("[[File:"):
			start = True
		if start:
			if disambig:
				pstring += "> **This is a disambiguation page.**\n"
				break
			elif lc < maxlines:
				lc += 1
				pstring += "> " + html.unescape(l)
				pstring += "\n"
	
	ret += "> # **{}**\n\n".format(re.sub(r'(.*)', urlize, title))
	if title.lower() != q.lower():
		redir = "> *Redirected from {}*\n\n".format(
			re.sub(r'(.*)', urlize, q))
		redirurl = re.search('https://wiki\.factorio\.com/.*', redir)
		redir = re.sub(r'(\W)(\w)',r'\1^\2', redir)
		redir = re.sub(r'\^https://.*', redirurl.group(0), redir)
		ret += redir
	pstring = re.sub(r'\[\[([^\]]*)\]\]', urlize, pstring)
	pstring = re.sub(r'\'\'\'', '**', pstring)
	pstring = re.sub(r'\'\'', '*', pstring)
	if pstring != "":
		ret += '{}\n'.format(pstring)
	ret += "*****\n\n"
	return ret
	