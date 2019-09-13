#!/bin/bash
set -e


# Note above that we run dumb-init as PID 1 in order to reap zombie processes
# as well as forward signals to all processes in its session. Normally, sh
# wouldn't do either of these functions so we'd leak zombies as well as do
# unclean termination of all our sub-processes.
# As of docker 1.13, using docker run --init achieves the same outcome.

VERSION=latest
echo $VERSION

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

function hub(){
        config_volumes=()
        CONTAINER_USER_DIR='/root' # Or use '/' if mapping an imaginary user that won't have a home folder inside
        for config in ${HOME}/.gitconfig*; do
            config_volumes+="--mount type=bind,source=${HOME}/$(basename $config),target=${CONTAINER_USER_DIR}/$(basename $config) ";
        done
        # The space before the final " is SIGNIFICANT for proper concatenation

        docker run -it --rm \
                ${config_volumes[@]} \
                --mount type=bind,source="${HOME}/.ssh/",target="${CONTAINER_USER_DIR}/.ssh/",readonly \
                --mount type=bind,source="$(dirname $SSH_AUTH_SOCK)",target="$(dirname $SSH_AUTH_SOCK)" \
                -w "${HOME}" \
                -e "SSH_AUTH_SOCK=$SSH_AUTH_SOCK" \
                -u root:$(id -g $USER) \
                --log-driver none \
                --name git \
                --entrypoint git \
                alpine/git  "$@"

        echo "here"
        # Can't use the upstream to push/fetch/clone until the above mentioned PR #46 w/ ssh gets merged
        # Also the PAGER=less won't work without that getting added into #46 or another PR
}

alias git="hub "