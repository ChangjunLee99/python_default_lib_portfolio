import subprocess
import sys

def install_requirements():
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print('��� ��Ű���� ���������� ��ġ�Ǿ����ϴ�.')
    except subprocess.CalledProcessError as e:
        print(f'��Ű�� ��ġ �� ������ �߻��߽��ϴ�: {e}')
    except FileNotFoundError:
        print('requirements.txt ������ ã�� �� �����ϴ�.')

if __name__ == '__main__':
    install_requirements()
