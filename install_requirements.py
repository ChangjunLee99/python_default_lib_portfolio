import pip
with open("requirements.txt", "r") as f:
    for line in f:
        line = line.strip()
        if line:
            pip.main(['install', '-U', line])
