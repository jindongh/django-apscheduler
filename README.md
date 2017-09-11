Django APScheduler
================================

![Build status](http://travis-ci.org/jindongh/django-apscheduler.svg?branch=master)
[![codecov](https://codecov.io/gh/jindongh/django-apscheduler/branch/master/graph/badge.svg)](https://codecov.io/gh/jindongh/django-apscheduler)
[![PyPI version](https://badge.fury.io/py/django_apscheduler.svg)](https://badge.fury.io/py/django_apscheduler)

`APScheduler <https://github.com/agronholm/apscheduler>`_ for `Django <https://github.com/django/django>`_.

This little wrapper around APScheduler enables storing persistent jobs in the database using Django's ORM rather than requiring SQLAlchemy or some other bloatware.

It is a fork of https://github.com/jarekwg/django-apscheduler project (thanks to author), which had some errors, no tests, no PyPI package.

Features in this project:

* Work on both python2.* and python3+
* Manage jobs from Django admin interface
* Monitor your job execution status: duration, exception, traceback, input parameters.

Usage
-----

* Install ``django_apscheduler``:
  ```python
  pip install git+https://github.com/jindongh/django-apscheduler.git
  ```

* Add ``django_apscheduler`` to ``INSTALLED_APPS`` in your Django project settings:
  ```python

  INSTALLED_APPS = (
    ...
    django_apscheduler,
  )
  ```
  
* Run migrations:
  ```python
  ./manage.py migrate
  ```
* Instanciate a new scheduler as you would with APScheduler. For example:
  ```python
  from apscheduler.schedulers.background import BackgroundScheduler
  
  scheduler = BackgroundScheduler()
  ```
* Instruct the scheduler to use ``DjangoJobStore``:
  ```python

  from django_apscheduler.jobstores import DjangoJobStore
  
  # If you want all scheduled jobs to use this store by default,
  # use the name 'default' instead of 'djangojobstore'.
  scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
  ```
  
* If you want per-execution monitoring, call register_events on your scheduler:
  ```python
  
    from django_apscheduler.jobstores import register_events
    register_events(scheduler)
  ```
  
  It gives you such interface:
  ![](http://dl3.joxi.net/drive/2017/05/19/0003/0636/258684/84/bebc279ecd.png)
  

* Register any jobs as you would normally. Note that if you haven't set ``DjangoJobStore`` as the ``'default'`` job store, you'll need to include ``jobstore='djangojobstore'`` in your ``scheduler.add_job`` calls.  
  
* Start the scheduler:
  ```python
  scheduler.start()
  ```
  
Full example:
```python
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.blocking import BlockingScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events

scheduler = BlockingScheduler()

scheduler.add_jobstore(DjangoJobStore())
scheduler.add_executor(ThreadPoolExecutor(10))

register_events(scheduler)

#will block you here because of BlockingScheduler usage
scheduler.start()

```
