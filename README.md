# 4442Testing
Software Testing Project for CS4442

## Setup
To run the program pull the docker image from the docker hub repository using
```shell
docker pull eoghano4321/iser_oracle_db:latest
```
Navigate to the folder containing the [dockerfile](dockerfile) and run the build command
```shell
docker build -t oracle-db-iser
```
You can then run the container and expose the ports using the command
```shell
docker run -d -p 1521:1521 -p 5500:5500 -e ORACLE_PASSWORD=root oracle-db-iser
```

You may need to change the service name in [main](src/main.py)
