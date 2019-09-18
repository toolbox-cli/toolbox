# -----------------------------------------------------------------------------
# DevOps Toolbox Base Image
# -----------------------------------------------------------------------------
FROM alpine:3.10.1
USER root

# Ensure the executable is installed into $BIN_DIR (which is part of the executable $PATH env down below)
# Otherwise the container entrypoint doesn't work as intended :/
ARG BIN_DIR=${BIN_DIR:-"/usr/local/bin"}
ARG GOSU_VERSION=${GOSU_VERSION:-"1.11"}
ARG VERSION=${VERSION:-"latest"}

ENV PATH="/usr/local/sbin:${BIN_DIR}:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:~/.local/bin" \
    VERSION=${VERSION}

RUN apk --no-cache add tzdata && \
    echo "America/New_York" | tee /etc/timezone && \
    ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime

RUN set -eux && \
    apk add --no-cache ca-certificates openssl dumb-init && \
    case "`arch`" in \
        aarch64) ARCH="arm64" ;; \
        armhf) ARCH="arm" ;; \
        x86) ARCH="386" ;; \
        x86_64) ARCH="amd64" ;; \
        *) echo >&2 "error: unsupported architecture: `arch`" && exit 1 ;; \
    esac && \
    export ARCH=$ARCH && \
    mkdir -p /tmp/build && \
    cd /tmp/build && \
    echo "Installing gosu v${GOSU_VERSION}" && \
    wget -O ${BIN_DIR}/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-${ARCH}" && \
    chmod +x ${BIN_DIR}/gosu && \
    rm -rf /tmp/build && \
    rm -rf /var/cache/apk/*

# devops doesn't need root privileges so we run it as the devops user from the
# entry point script. The entry point script also uses dumb-init as the top-level
# process to reap any zombie processes created by devops sub-processes.
COPY ./toolbox-handler.sh ${BIN_DIR}/toolbox-handler.sh

VOLUME /root

CMD [ "/bin/bash" ]

# You have to use the '["exec_location", "arg1", "arg2", ..., "argn"]' method so things exec properly.
# https://docs.docker.com/engine/reference/builder/#entrypoint
ENTRYPOINT ["toolbox-handler.sh"]