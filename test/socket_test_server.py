import sys
from os import path
sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ))

from lib.util import *
import socket

util = Util()
util.parsesys()
if util.findChild("PORT") != None:
    port = int(util.getValueStr("PORT"))
else:
    port = 5001
# 서버 설정
host = "127.0.0.1"  # 서버의 IP 주소 또는 도메인 이름
#port = 12345       # 포트 번호

# 서버 소켓 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)
#server_socket.settimeout(0.2)

print(f"서버가 {host}:{port}에서 대기 중입니다...")

while True:
    # 클라이언트 연결 대기
    try:
        client_socket, client_address = server_socket.accept()
        print(f"클라이언트 {client_address}가 연결되었습니다.")
        #client_socket.settimeout()
        # 클라이언트로부터 요청 받기
        while True:
            data = client_socket.recv(1024).decode("utf-8")
            if not data:
                continue
            

            # 요청 파싱
            parts = data.split("&&")
            if len(parts) != 0:
                name = parts[0]
                message = parts[1]
                response = f"어서와! {name}"

                # 클라이언트 이름과 메시지 출력
                print(f"클라이언트 이름: {name}")
                print(f"클라이언트 메시지: {message}")
            else:
                response = "유효하지 않은 요청"

            # 응답 클라이언트에게 전송
            client_socket.send(response.encode("utf-8"))

    except Exception as e:
        print(f"오류 발생: {e}")
        break

# 클라이언트 소켓 닫기
print("연결종료")
client_socket.close()
