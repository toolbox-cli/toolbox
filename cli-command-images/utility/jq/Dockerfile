FROM toolbox_base:latest
USER root

# Ensure the executable is installed into $BIN_DIR (which is part of $PATH in the base toolbox image layer)
# Otherwise the container entrypoint doesn't work as intended :/
ENV BIN_DIR=${BIN_DIR:-"/usr/local/bin"}

RUN apk add --no-cache curl && \
    mkdir -p ${BIN_DIR} && wget -O ${BIN_DIR}/jq \
    `curl -s https://api.github.com/repos/stedolan/jq/releases/latest | grep browser_download_url | cut -d '"' -f 4 | grep -i linux64` && \
    chmod +x ${BIN_DIR}/jq && \
    apk del curl && \
    rm -rf /var/cache/apk/*

# You have to use the '["exec_location", "arg1", "arg2", ..., "argn"]' method so things exec properly.
# https://docs.docker.com/engine/reference/builder/#entrypoint
ENTRYPOINT ["jq"]
