#!/usr/bin/dumb-init /bin/sh
set -e


# Note above that we run dumb-init as PID 1 in order to reap zombie processes
# as well as forward signals to all processes in its session. Normally, sh
# wouldn't do either of these functions so we'd leak zombies as well as do
# unclean termination of all our sub-processes.
# As of docker 1.13, using docker run --init achieves the same outcome.

echo "toolbox -- version $VERSION"

echo "$(id -u):$(id -g)"

set -- gosu $(id -u):$(id -g) "$@"

echo "1 command: $0 command @: $@"

set -- "$@"

echo "2 command: $0 command @: $@"

exec "$@"