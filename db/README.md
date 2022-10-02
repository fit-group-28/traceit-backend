# Set up

## Install

1. Install docker desktop via https://docs.docker.com/compose/install/compose-desktop/
2. `pip install psycopg2`

    **For mac m1**
    ```
    brew install libpq --build-from-source
    brew install openssl
    brew install postgres

    export LDFLAGS="-L/opt/homebrew/opt/openssl@1.1/lib -L/opt/homebrew/opt/libpq/lib"
    export CPPFLAGS="-I/opt/homebrew/opt/openssl@1.1/include -I/opt/homebrew/opt/libpq/include"

    pip3 install psycopg2
    ```

## Running docker image

1. start docker desktop
2. cd into db file
3. Create a volume `docker volume create database-data`
4. run command `docker-compose up -d`

## Modify database

1. cd into db file
2. run command `docker-compose run database bash`
3. run command `psql --host=database --username=postgres`
4. enter password `postgres`

## exit database

1. exit bash enter command `quit` -> `exit`
2. exit docker-compose by `ctrl-c` (MAC) or command `docker-compose down` (WIN)

## test for query database outside docker

1. run command `python ./test/db-connection-test.py`

## debug

1. On mac, if you see permission denied for init-database.sh permission denied, try `chmod 777 <file path to db>`
2. if connecting database failed, try `docker-compose down` and start again
