from lib.sql import *

class User(BaseModel):
	id      = Column(Integer,      primary_key=True)
	name    = Column(String(16),   doc="姓名")
	gender  = Column(db.CHAR(1),   doc="性别")
	phone   = Column(String(11),   doc="电话")
	email   = Column(String(16),   doc="QQ")