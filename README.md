# Devman-Bot
Отправляем уведомления о проверке работ.

## Как установить
    
1.Переименовать файл  `.env.example` в `.env`.
    
2.Добавить учетный данные в файл `.env`

`TELEGRAM_TOKEN`  -   токен вашего бота

`TELEGRAM_CHAT_ID` -  id аккаунта, куда должны приходить уведомления
        
`DEVMAN_TOKEN`    -   токен с [dvmn.org](https://dvmn.org/api/docs/)
    
3.Python3 должен быть уже установлен. 

Затем используйте pip (или pip3, есть есть конфликт с Python2) для установки зависимостей:
   
    pip install -r requirements.txt
    
## Как пользоваться

    python main.py

## Размещение на Heroku

1. Создаем [новое](https://dashboard.heroku.com/new-app) приложение.

2. Переходим в `Deploy`, подключаем репозиторий github.

3. Нажимаем `Deploy Branch`.

4. Устанавливаем и авторизовываемся в [heroku-cli](https://devcenter.heroku.com/articles/heroku-cli#download-and-install).

5. Прописываем переменные из `.env.example` в `Settings` -> `Config Vars`.

6. Выполняем:
```
heroku ps:scale bot=1 -a Имя_приложения
```

### Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org).
