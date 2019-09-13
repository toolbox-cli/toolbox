FROM toolbox_base:latest
USER root

# Ensure the executable is installed into $BIN_DIR (which is part of $PATH in the base toolbox image layer)
# Otherwise the container entrypoint doesn't work as intended :/
ENV BIN_DIR=${BIN_DIR:-"/usr/local/bin"}
ENV ANSIBLE_VERSION=${ANSIBLE_VERSION:-"2.8.3"}
COPY ./requirements.txt .

RUN echo "===> Adding Python runtime..."  && \
    apk --update add python py-pip openssl ca-certificates    && \
    apk --update add --virtual build-dependencies \
                python-dev libffi-dev openssl-dev build-base  && \
    pip install --upgrade pip cffi                            && \
    \
    \
    echo "===> Installing Ansible..."  && \
    pip install ansible                && \
    apk del build-base && \
    rm -rf /var/cache/apk/*

# You have to use the '["exec_location", "arg1", "arg2", ..., "argn"]' method so things exec properly.
# https://docs.docker.com/engine/reference/builder/#entrypoint
ENTRYPOINT ["ansible"]
