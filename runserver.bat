@echo off
cmd /k "cd /d C:venv\Scripts & activate & cd /d C:\Users\dfaww\PycharmProjects\API_Surplus &  python manage.py runserver & python -m pytest -v --html-report=./report/report.html"
