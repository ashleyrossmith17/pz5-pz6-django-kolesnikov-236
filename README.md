# Учебный портал · ПЗ5 и ПЗ6

Колесников Кирилл Петрович, М3О-236БВ-25.

Django 5.2, SQLite, Tabler 1.4.0 и Chart.js 4.4.8. Проект содержит списки курсов,
факультетов и групп, вход, профиль, создание, изменение и удаление записей,
аналитику и фильтрацию по факультетам. Внешние CSS/JS сохранены в static/vendor:
для запуска сайта не нужен доступ к CDN.

## Запуск в Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
$env:DEMO_PASSWORD = Read-Host 'Пароль для локальных учебных пользователей'
python manage.py seed_demo
python manage.py runserver 127.0.0.1:8000
```

Открыть http://127.0.0.1:8000/login/. Логин методиста: `kolesnikov`, пароль задан
через `DEMO_PASSWORD`. Есть также `student1`–`student4` и `administrator`.
Повторный seed_demo обновляет учебные данные и не сбрасывает пароли.
Пользователи с ролью «Студент» могут просматривать страницы, но не менять записи.

## Этапы практических работ

ПЗ5: `/login/?ui=classic` переключает исходное оформление; `?ui=tabler` включает
Tabler. Выбор сохраняется в сессии. В обоих режимах работают одни и те же
представления, формы и база данных. Примеры: `/`, `/courses/`, `/departments/`,
`/groups/`, `/courses/add/`, `/courses/1/edit/`.

ПЗ6: `/dashboard/` показывает четыре метрики и три диаграммы.
GET-параметр `department` фильтрует курсы, группы и пользователей по факультету.
Пользователи без группы включены в общую статистику, но не относятся к отдельному
факультету. Данные передаются в JavaScript через Django `json_script`.

```powershell
python manage.py check
python manage.py test
```

Настройки предназначены для локальной учебной работы. Для публикации на сервере
задайте DJANGO_SECRET_KEY, DJANGO_DEBUG=0 и настройте ALLOWED_HOSTS/HTTPS.

## Источники библиотек

- Django: https://docs.djangoproject.com/en/5.2/
- Tabler: https://docs.tabler.io/ui/getting-started/installation/
- Chart.js: https://www.chartjs.org/docs/latest/
- Lucide: https://lucide.dev/

Лицензии внешних библиотек сохранены рядом с файлами в static/vendor.
