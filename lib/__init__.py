
if __name__ == '__main__':
	if __package__ is None or __package__ == '':
		from Obj import *
		from lib.MariaDBCon import *
		from lib.SQLite3Con import *
		from util import *
		from base_protocol import *
	else:
		from .Obj import *
		from .MariaDBCon import *
		from .SQLite3Con import *
		from .util import *
		from .base_protocol import *
else:
	from .Obj import *
	from .MariaDBCon import *
	from .SQLite3Con import *
	from .util import *
	from .base_protocol import *

#DGo()	
#dg = DGo()
#print("hello world!")