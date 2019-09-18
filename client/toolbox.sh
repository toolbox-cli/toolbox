#!/bin/bash
set -e


# Note above that we run dumb-init as PID 1 in order to reap zombie processes
# as well as forward signals to all processes in its session. Normally, sh
# wouldn't do either of these functions so we'd leak zombies as well as do
# unclean termination of all our sub-processes.
# As of docker 1.13, using docker run --init achieves the same outcome.

VERSION=latest

function docker_alias() {
    docker run \
        -it \
        --rm \
        -v $HOME:$HOME:z \
        -v /tmp/.X11-unix:/tmp/.X11-unix:z \
        -e DISPLAY=$DISPLAY \
        -w $HOME \
        -u "$(id -u):$(id -g)" \
        --net=host \
        ${@} || echo "Docker command '${1} ${2} ...' failed!"
}

alias eclipse="docker_alias fgrehm/eclipse:v4.4.1 eclipse"
# JavaScript / CoffeeScript
alias node="docker_alias node node"
alias npm="docker_alias node npm"
alias coffee="docker_alias shouldbee/coffeescript coffee"

# PHP
alias php="docker_alias php php"

# Ruby
alias ruby="docker_alias ruby ruby"

alias rails="docker_alias rails rails"
alias rake="docker_alias rails rake"

# Python
alias python2.7="docker_alias python:2.7 python"
alias python="docker_alias python python"

alias django-admin.py="docker_alias django django-admin.py"

# Redis
alias redis-cli="docker_alias redis redis-cli"
alias redis-server="docker_alias redis redis-server"

alias redis-benchmark="docker_alias redis redis-benchmark"
alias redis-check-dump="docker_alias redis redis-check-dump"
alias redis-check-aof="docker_alias redis redis-check-aof"
alias redis-sentinel="docker_alias redis redis-sentinel"

# MongoDB
alias mongo="docker_alias mongo mongo"
alias mongod="docker_alias mongo mongod"

# Postgres
alias postgres="docker_alias postgres postgres"
alias psql="docker_alias postgres psql"

alias pg_dump="docker_alias postgres pg_dump"
alias pg_dumpall="docker_alias postgres pg_dumpall"
alias pg_restore="docker_alias postgres pg_restore"

# Nginx
alias nginx="docker_alias nginx nginx"

# LAMP
alias lamp-here="docker_alias /var/www/html tutum/lamp"

# TFlint - https://github.com/wata727/tflint
alias tflint="docker_alias /data wata727/tflint"
