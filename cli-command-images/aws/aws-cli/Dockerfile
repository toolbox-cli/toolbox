FROM toolbox_base:latest
USER root

# Ensure the executable is installed into $BIN_DIR (which is part of $PATH in the base toolbox image layer)
# Otherwise the container entrypoint doesn't work as intended :/
ENV BIN_DIR=${BIN_DIR:-"/usr/local/bin"}

RUN apk add --no-cache curl python3 groff && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
    cd /tmp/ && \
    curl "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "awscli-bundle.zip" && \
    unzip awscli-bundle.zip && \
    ./awscli-bundle/install -i /usr/local/aws -b ${BIN_DIR}/aws && \
    chmod +x ${BIN_DIR}/aws

# You have to use the '["exec_location", "arg1", "arg2", ..., "argn"]' method so things exec properly.
# https://docs.docker.com/engine/reference/builder/#entrypoint
ENTRYPOINT ["aws"]