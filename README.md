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
* Create a heroku remote if you haven't already:
** `heroku git:remote -a pompom-prod`
* Deploy to heroku using `git push heroku master`
* If deploying for the first time, add a superuser to the application in order to access the backend `heroku run python manage.py createsuperuser`

### DNS setup

Follow the Heroku instructions here:
https://devcenter.heroku.com/articles/custom-domains#configuring-dns-for-root-domains

For GoDaddy, we tried having root domain 'forwarded' with GoDaddy's tools, but Heroku was never able to verify.
What we're trying now is to ahve GoDaddy forward the naked domain to www. and then have heroku handle it from there.  (eg http://pompomapp.net forwards to http://www.pompomapp.net/ which has its records that point to heroku's nameservers)

In order to enable automatic ssl management, be sure to use the '.herokudns.com' domains when forwarding

### Email setup
The admin password recovery feature sends email, which is configured in Heroku to use mailgun.  https://elements.heroku.com/addons/mailgun
`heroku addons:create mailgun:free`
The free tier is good for up to 10,000 emails per month.
Prod environments should override the DJANGO_EMAIL_BACKEND environment variable to 'django.core.mail.backends.smtp.EmailBackend' to enable sending real emails.

Emails won't work generally for the dev account, unless you go to mailgun (via heroku) and add your account as an Authorized Recipient.

To enable emails, set the heroku env variables like so:
EMAIL_HOST=$MAILGUN_SMPT_SERVER
EMAIL_PORT=$MAILGUN_SMTP_PORT
EMAIL_HOST_USER=$MAILGUN_SMTP_LOGIN
EMAIL_HOST_PASSWORD=$MAILGUN_SMTP_PASSWORD

When adding the txt/mx records described here https://app.mailgun.com/app/domains/mg.pompomapp.net/verify
Note: godaddy showed an error when saving, but saved the records anyway.