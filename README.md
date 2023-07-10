# CRAIS-PESU
Website for CRAIS of PES University


## Deployment Instructions

### Using Docker
1. Create an `.env.prod` file with the following environment variables.

```
DEBUG=0
SUPERUSER_USERNAME="admin username"
SUPERUSER_PASSWORD="admin password
ALLOWED_HOSTS="localhost,127.0.0.1,crais.pes.edu,other hosts"
EMAIL_HOST_USER="email address associated with site to send emails. This can be skipped and if skipped, it will not send any emails for form responses. If skipping, comment line 215-219 in settings.py"
EMAIL_HOST_PASSWORD="email app password - need to create an email and create an application password"
DATABASE_URL="database url - database must exist. exampele `postgres://username:passowrd@host:5432/database-name`
```

2. Run `docker compose -f docker-compose.prod.yaml up`

3. At this point, you will have gunicorn running on port 8000, now use nginx as a reverse proxy to proxy pass every http request to port 8000.
You can also enable https using `lets encrypt` or other ways managed by DNS provider (example: cloudflare).

Example nginx config:
```yaml
http {
        server {
                listen 80;
                root /data;


        location / {
                proxy_pass http://localhost:8000/;
                client_max_body_size 20m;
        }
    }
}

events {}
```

### Without using docker
1. pre-requisites
```
python3.11
poetry (1.5>)
nodejs 20
npm
```

2. Install project dependencies by running
`poetry install --without dev`

3. compile tailwind styles with the following commands

```
# change directory to tailwind
cd tailwind

# install packages
npm i

# compile styles
npm run build:css
```

3. Now back in the root directory, run the following to collect all static files

    `python manage.py collectstatic --no-input --clear`

    This will also run `manage.py migrate` automatically.

4. Run gunicorn server

    `gunicorn crais.wsgi:application --bind 0.0.0.0:8000`

5. Now setup nginx to proxy pass requests to localhost:8000 as shown in the above docker section.

The number of workers gunicorn spawns can be altered based on the deployment machine specs as highlight here in the docs: https://docs.gunicorn.org/en/stable/design.html#how-many-workers


## Local Development Instructions
1. run `docker compose -f docker-compose.dev.yaml up`. It runs an instance of the django server and postgres database.
