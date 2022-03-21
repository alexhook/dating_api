Dating API
===========

Ссылки
-----------
1. https://tests-alex-maksimeniuk.ru/api/clients/create
2. https://tests-alex-maksimeniuk.ru/api/list
3. https://tests-alex-maksimeniuk.ru/api/clients/{id}/match

MySQL
----------
Для подключения MySQL необходимо в корневой папке создать файл .db.cnf со следующим содержанием:  

    # .db.cnf
    [client]
    database = dating
    user = django
    password = password
    default-character-set = utf8
    
Или заменить в файле settings.py строки:  

    ...
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'OPTIONS': {
                'read_default_file': '.db.cnf',
            },
        }
    }
    ...

На следующие:  

    ...
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'dating',
            'USER': 'django',
            'PASSWORD': 'password',
            'HOST': 'localhost',
        }
    }
    ...
