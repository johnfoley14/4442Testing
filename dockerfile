# Basic dockerfile to run the database
FROM eoghano4321/iser_oracle_db:latest

ENV ORACLE_PASSWORD=root
ENV ORACLE_SID=XE

ADD init.sql /docker-entrypoint-initdb.d/

EXPOSE 1521/tcp
EXPOSE 5500/tcp