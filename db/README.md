# Set up

## Install

1. Install docker desktop via https://docs.docker.com/compose/install/compose-desktop/

## Running docker image

1. cd into db file
2. run command `docker-compose up`

## Modify database

1. cd into db file
2. run command `docker-compose run database bash`
3. run command `psql --host=database --username=postgres`
4. enter password `postgres`

## exit database

1. exit bash enter command `quit` -> `exit`
2. exit docker-compose by `ctrl-c` (MAC) or command `docker-compose down` (WIN)
