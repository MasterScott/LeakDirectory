# LeakDirectory

The purpose of this application is to index globaleaks nodes and receivers.

## Installation

```
pip install -r requirements.txt
python manage.py syncdb
```

To start the django web application in development mode:

```
python manage.py runserver
```

To start the celery task manager run:

```
celery worker --app=leakdirectory -l info
```
