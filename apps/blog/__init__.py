from .front import DefaultHandler, MineHandler

def upload_handle(handler):
	if handler.is_get:
		return handler.render()
	else:
		file = handler.request.files['file']
		return file.save('/home/an/Downloads/' + file.filename)