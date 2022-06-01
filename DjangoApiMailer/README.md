# API сервер для отправки рассылок и получения статистики
## Точки доступа:

>GET: "API/clients/" -> resp_data
```
resp_data = [
    {
        "id": 1,
        "tags": [
                "sometag"
            ],
        "phone": 79998887766,
        "phone_code": 999,
        "time_zone": 3
    }
]
```
>GET: /api/clients/1 -> resp_data
```
resp_data = {
    "id": 1,
    "tags": [
        "sometag"
    ],
    "phone": 79998887766,
    "phone_code": 999,
    "time_zone": 3
}
```
>POST: localhost:8000/api/clients/: req_data -> resp_data 
```
req_data = {
    "phone": "79997654321",
    "phone-code": "999",
    "tags": ["anytag"],
    "time_zone": 5
}
```
```
resp_data = {
    "id": 4,
    "tags": [
        "anytag"
    ],
    "phone": 79997654321,
    "phone_code": 999,
    "time_zone": 5
}
```

>GET: "/api/mailings" -> resp_data 
```
resp_data = [
    {
        "id": 1,
        "messages": [
            {
                "id": 1,
                "client": {
                    "id": 2,
                    "tags": [
                        "tag"
                    ],
                    "phone": 79876543210,
                    "phone_code": 987,
                    "time_zone": 3
                },
                "status": false,
                "sent_time": "2022-05-31T20:32:05+03:00",
                "mailing": 1
            }
        ],
        "start": "2022-05-31T14:27:27+03:00",
        "text": "Какой-то текст для рассылки",
        "end": "2022-05-31T23:00:00+03:00"
    }
]
```
> GET: "/api/mailings/1" -> resp_data 
``` 
resp_data = {
    "id": 1,
    "messages": [
        {
            "id": 1,
            "client": {
                "id": 2,
                "tags": [
                    "tag"
                ],
                "phone": 79876543210,
                "phone_code": 987,
                "time_zone": 3
            },
            "status": false,
            "sent_time": "2022-05-31T20:32:05+03:00",
            "mailing": 1
        }
    ],
    "start": "2022-05-31T14:27:27+03:00",
    "text": "Какой-то текст для рассылки",
    "end": "2022-05-31T23:00:00+03:00"
}
```
>POST: /api/mailings/: req_data -> resp_data 
``` 
req_data = {
    "clients": {
            "ids": [1],
            "phones": ["79998887766"],
            "tags": ["sometag"],
            "time_zones": [3],
            "phone_codes": [999]
        },
    "start": "2022-06-01 16:00",
    "text": "Текст для рассылки",
    "end": "2022-06-01 21:00"
}
```
```
resp_data = {
    "id": 4,
    "messages": [
        {
            "id": 3,
            "status": false,
            "sent_time": "2022-06-01T13:15:28+03:00",
            "mailing": 4,
            "client": 1
        }
    ],
    "start": "2022-06-01T16:00:00+03:00",
    "text": "Текст для рассылки",
    "end": "2022-06-01T21:00:00+03:00"
}
```
## Для запуска:

```
# Установить docker
> sudo apt remove docker docker-engine docker.io containerd runc # удалит старую версию, если есть
> sudo apt update && sudo apt upgrade -y # обновит список пакетов
> sudo apt install \
  apt-transport-https \
  ca-certificates \
  curl \
  gnupg-agent \
  software-properties-common -y # установит необходимые пакеты для загрузки через https 
> curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - # ОК 
> sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" # посмотреть подходящую версию можно на сайте https://download.docker.com/
> sudo apt update && sudo apt upgrade -y
> sudo apt install docker-ce docker-compose -y 
> sudo systemctl enable docker
# эта команда скачает скрипт для автоматической установки докера 
> curl -fsSL https://get.docker.com -o get-docker.sh
> sh get-docker.sh # эта команда запустит его sh get-docker.sh

# Установить зависимости проекта:
> pip install -r requirements.txt 

# Запуск celery:
> docker-compose up -d --build # <-d>. Фоновый режим <--build>.
> celery -A DjangoApiMailer beat  # <DjangoApiMailer>. - название таска, обычно по названию проекта.
> celery -A DjangoApiMailer worker -l INFO --pool=solo  # <DjangoApiMailer>. - название таска, обычно по названию проекта. <INFO>. - уровень логирования https://khashtamov.com/ru/python-logging/

# Запуск сервера:
> python manage.py runserver 
```
