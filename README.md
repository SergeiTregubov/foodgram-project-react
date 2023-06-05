# praktikum_new_diplom

### **Адрес сайта на Яндекс.Облаке:**
http://158.160.102.89/signin Вход на сайт и регистрация <br>
http://158.160.102.89/recipes Главная страница рецептов <br>
http://158.160.102.89/subscriptions Подписки <br>
http://158.160.102.89/recipes/create Создание рецепта <br>
http://158.160.102.89/favorites Избранное <br>
http://158.160.102.89/cart Список покупок <br>
---
### **Данные для входа в админку:**
```
Имя: Sergei
Фамилия: Tregubov
Имя пользователя: SergeiTregubov
Адрес электронной почты: g@bk.ru
Пароль: 1234
```


### **Спецификация API Foodgram**
Документация: http://localhost/api/docs/
---

# Дипломный проект. Python backend разработчик.

### Описание

Сервис Foodgram для публикации рецептов. Сайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов.

### Используемые технологии:
![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![image](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![image](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![image](https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white)
![image](https://img.shields.io/badge/VSCode-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white)
![image](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)
![image](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![image](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)
![image](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
### 
1) Инструкция по установке:

## Локальная установка:
- Клонируем репозиторию на компьютер:

```bash
1) git@github.com:SergeiTregubov/foodgram-project-react.git
```
```
2) cd foodgram-project-react
```

- Cоздать и активировать виртуальное окружение:

```bash
python -m venv venv
```

```bash
source venv/Scripts/activate - Windows
```
```
source venv/bin/activate - Linux systems
```
- Установить зависимости проекта:

```bash
cd backend/foodgram/
```
```
pip install -r requirements.txt
```

- Создать и выполнить миграции:
```bash
python manage.py makemigrations
```
```
python manage.py migrate
```

- Запуск сервера локально:
```bash
python manage.py runserver
```

### **Команды докера**
```
sudo docker-compose up -d --build
sudo docker-compose down -v
sudo docker-compose stop
sudo docker-compose start
docker container ls -a
docker image ls -a
docker container rm
docker image rm
```