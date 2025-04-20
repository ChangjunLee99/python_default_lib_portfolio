
if __name__ == '__main__':
	if __package__ is None or __package__ == '':
		from api import *
	else:
		from .api import *
else:
    from .api import *
