

from ctypes import *
from ctypes.wintypes import *

# windows 의 kernel32.dll 동적 라이브러리를 로드한다.
kernel32dll = windll.LoadLibrary("D:\\develop\\python_default_lib\\kernel32.dll")

# 동적 라이브러리 객체에서 함수 포인터를 얻는다. (현재 프로세스 ID 수집 함수)
pfGetCurrentProcessId = getattr(kernel32dll, 'GetCurrentProcessId')

MyProcessId = pfGetCurrentProcessId()
print('My Process ID : {0}'.format(MyProcessId))

pfProcessIdToSessionId = getattr(kernel32dll, 'ProcessIdToSessionId')

pfProcessIdToSessionId.argtypes = [DWORD, PDWORD]

# windows 세션 아이디 값을 받을 변수를 정의한다.
MySessionId = DWORD() 

# 함수를 호출한다. (두 번째 인자는 포인터이므로 byref method 로 처리)
pfProcessIdToSessionId(MyProcessId, byref(MySessionId))

# windows 세션 ID를 출력한다.
print('My Session Id : {0}'.format(MySessionId.value))