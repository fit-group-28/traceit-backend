FROM postgres
COPY ./sql/init-database.sh /docker-entrypoint-initdb.d/init-database.sh
CMD ["init-database.sh", "postgres"]
