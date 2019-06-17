# galgantar.tk
Online schedule web application written in Flask (python) and deployed on Heroku.

Link: [galgantar.tk](http://galgantar.tk)

## Commands
Commands (defined in Procfile) used for faster manual process execution

Manually clean database (process also used for scheduled database cleaning)
```
heroku run clean
```

Manually send email
```
heroku run send
```

### Manual database executions:
List User database
```
heroku run execute -user
```
List Confirmations databae
```
heroku run execute -confirm
```
Execute query in query.sql
```
heroku run execute -sql
```

## Built with
* [Flask](http://flask.pocoo.org/) (framework)
* [PostgreSQL](https://www.postgresql.org/) (SQL database)
* [psycopg2](http://initd.org/psycopg/) (database connection)
* [Bcrypt](https://pypi.org/project/bcrypt/) (hashing)
* [Bootstrap](https://getbootstrap.com/) (front-end)
