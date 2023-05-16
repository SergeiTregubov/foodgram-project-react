# praktikum_new_diplom
### 1) Инструкция по установке:

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
