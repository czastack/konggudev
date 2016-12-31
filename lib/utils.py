import time

def get_item(items, key):
	"""
	用元组或列表第一个元素作为键获取
	"""
	for item in items:
		if item[0] == key:
			return item[1]

def timestr(t, show_time = True):
    """ 
    时间戳转日期字符串
    :p show_time: 是否显示时分秒
    """
    ltime=time.localtime(t)
    fmt = "%Y-%m-%d"
    if show_time:
        fmt += " %H:%M:%S"
    return time.strftime(fmt, ltime)