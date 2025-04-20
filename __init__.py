
if __name__ == '__main__':
	if __package__ is None or __package__ == '':
		from lib import *
	else:
		from .lib import *
else:
    from .lib import *
