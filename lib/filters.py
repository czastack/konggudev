import re
from jinja2.utils import Markup

def br(text):
	return Markup(re.sub('\n', '<br>', text))

def spacebr(text):
	return Markup(re.sub(' ', '<br>', text))

def strcut(text, length, end = '...'):
	if len(text) < length:
		return text
	return text[:length] + end

FILTERS = (br, spacebr, strcut)