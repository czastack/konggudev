import collections
Menu = collections.namedtuple('Menu','url title')

backend_side_menu = (
	Menu('@apply/setting', '招新部门设置'),
	Menu('@apply/list', '招新报名情况'),
)