import collections
Menu = collections.namedtuple('Menu','name title')

backend_side_menu = (
	Menu('setting', '招新部门设置'),
	Menu('info', '招新报名设置'),
	Menu('list', '招新报名情况'),
)