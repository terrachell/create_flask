#!/usr/bin/env python3
import os
import sys
cwd = os.getcwd()
if int(sys.version.split()[0].split('.')[1]) < 12:
    print("Для работы скрипта нужен python версии не менее 3.12.X")
    sys.exit(0)
os.system(f"sudo ln -s {cwd}/create-flask /usr/local/bin/create-flask")
print("Программа успешно установлена в систему")