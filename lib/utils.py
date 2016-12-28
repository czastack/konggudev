
def get_item(items, key):
	for item in items:
		if item[0] == key:
			return item[1]