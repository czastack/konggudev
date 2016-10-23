
def index_handle(handler):
	return handler.render('index')

def edit_handle(handler):
	return handler.render()

def test_handle(handler):
	return handler.json({"task": "上学/go"})