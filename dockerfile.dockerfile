FROM postgres:latest

ENV POSTGRES_DB=spotify_data
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=qwerty123

COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
