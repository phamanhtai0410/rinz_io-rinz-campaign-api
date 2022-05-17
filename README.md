# **RinZ Compaign API**

## Environment
- docker
- docker-compose

### Notes
- Changes in docker-compose.yml: exposed port, image name, container name
- Changes in supervisord.conf: log files' location

### Use with docker, docker-compose
JUST RUN: `> docker-compose up -d --build`

## Health check
```curl -i <prefix>/common/health_check```

## Container env config:
```/webapps/.env```