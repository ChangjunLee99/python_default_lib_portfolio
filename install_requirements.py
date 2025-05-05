import subprocess
import sys

def install_requirements():
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print('모든 패키지가 성공적으로 설치되었습니다.')
    except subprocess.CalledProcessError as e:
        print(f'패키지 설치 중 오류가 발생했습니다: {e}')
    except FileNotFoundError:
        print('requirements.txt 파일을 찾을 수 없습니다.')

if __name__ == '__main__':
    install_requirements()
