# Market
Customer to customer(c2c) marketplace based on Django.
## Installation
Install redis, check https://redis.io for your information.

You may need [this Chrome extension](https://chrome.google.com/webstore/detail/rss-subscription-extensio/nlbjncdgjeocebhnmkbbbdekmmmcbfjd/related?hl=en) for RSS subscription.
```text
$ git clone https://github.com/ndsf/Market
$ cd Market
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver
```
