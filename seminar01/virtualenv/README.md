## virtualenv. Основные моменты:
1. [Документация](https://virtualenv.pypa.io/en/latest/)
2. `virtualenv -p python3 <path_to_env>`
3. `source <path_to_env>/bin/active`
4. Далее установка через `pip` будет в `virtualenv`


## pip. Основные моменты
1. `pip install <package>`
2. `pip install -r requirements.txt`
3. `pip install -e requirements.txt`
4. `pip install -c constraints.txt`
5. `pip list` и `pip freeze` 
6. `pip install ipykernel && ipython kernel install --name=seminar1_project`



## Свой пакет на питоне
1. Нужно написать `setup.py`
2. Использование `setuptools`
3. Установить в `virtualenv`
4. Вместе с kernel-ом будет работать старый блокнот
