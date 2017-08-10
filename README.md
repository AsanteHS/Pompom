# pompom

[![build status](//gitlab.devartis.com/samples/django-sample/badges/master/build.svg)](http://gitlab.devartis.com/samples/django-sample/commits/master)

## Requirements

* Python >= 3.4
* pip
* [virtualenv](https://virtualenv.readthedocs.org/en/latest/installation.html)/[virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/)
  * `sudo pip install virtualenvwrapper`
  * add `source /usr/local/bin/virtualenvwrapper.sh` to your shell config (.bashrs or .zshrs)
  * restart your terminal

## Local Settings

* copy settings/local_example.py to settings/local.py.
  * `cp conf/settings/local_example.py conf/settings/local.py`
* copy settings/.env.default_local to settings/.env
  * `cp conf/settings/.env.default_local conf/settings/.env`

## Local setUp

* `mkvirtualenv pompom` or `workon pompom`
* `pip install -r requirements/local.txt`
* `export DJANGO_SETTINGS_MODULE=conf.settings.local`
* `./manage.py migrate`

## Run server

* `./manage.py runserver`

## Run tests

* `py.test`

## Run Lint/Style/CPD

Install `nodejs` and run `npm install`

* pylint: `sh scripts/python_lint.sh`
* cpd: `sh scripts/jscpd.sh`
* eslint: `sh scripts/eslint.sh`

## Git hooks

* Download the binary from [git-hooks](https://github.com/git-hooks/git-hooks/releases) and append it to your PATH.
* Install hooks: `git hooks install`

## Pycharm IDE

* config virtualenv created before as the virtualenv of the project (settings -> python interpreter)
* enable django support: settings -> django 
  * django project root: /home/diego/dev/projects/python/pompom
  * settings: conf/settings/local.py
  * manage script: manage.py
* mark directory Templates as "Templates folder" (right-click over directory in the "Project view")

## Deployment

### Add a database to the Heroku application

* Go to the Resources tab
* Under the Add-ons section search for `Heroku Postgres`
* Select a Plan name. Hobby tier might be enough for the application needs, but you should check: https://devcenter.heroku.com/articles/heroku-postgres-plans

### Add environment variables to your Heroku application

* Go to the Settings tab
* In the Config Variables click Reveal
* If you added the Postgres instance correctly you should see a `DATABASE_URL` entry.
* Add an entry named `DJANGO_SETTINGS_MODULE` with the value `conf.settings.production`
* Add an entry named `RAVEN_DSN` with the Sentry logging URL.

### Deployment using Gitlab

Gitlab already has a configured pipeline to make deployment easy and secure. Once you have tested the application on the staging environment and you are read to deploy, follow these steps:

* Create a tag in git. `git tag v0.1.0`
* Push it to gitlab's remote. `git push --tags`
* A new pipeline will run in Gitlab, once it succeeds you can manual deploy to production using the Deploy button.

### Deployment using Heroku

* Make sure you have successfully deployed and tested the current version to the staging environment.
* Locally run CI tasks. Including eslint, jscpd, tests and migrations.
* Create a tag in git. `git tag v0.1.0`
* Push it to gitlab's remote. `git push --tags`
* Deploy to heroku using `git push heroku master`
* Add a superuser to the application in order to access the backend `heroku run python manage.py createsuperuser`

