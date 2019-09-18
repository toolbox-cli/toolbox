FROM toolbox_aws-cli:latest
USER root

# Ensure the executable is installed into $BIN_DIR (which is part of $PATH in the base toolbox image layer)
# Otherwise the container entrypoint doesn't work as intended :/
ENV BIN_DIR=${BIN_DIR:-"/usr/local/bin"}

RUN echo "===> Adding Python runtime..."  && \
    apk --update add curl python py-pip openssl ca-certificates    && \
    apk --update add --virtual build-dependencies \
                python-dev libffi-dev openssl-dev build-base  && \
    pip install --upgrade pip cffi                            && \
    cd /tmp/

RUN echo "===> Adding SAML modules..."  && \
    apk add --no-cache libxml2-dev py-lxml && \
    python -m pip install boto3 boto requests_ntlm requests BeautifulSoup4 lxml configparser && \
    apk del build-base && \
    rm -rf /var/cache/apk/*

ADD ./aws_saml.py ${BIN_DIR}/aws_saml.py
RUN chmod +x ${BIN_DIR}/aws_saml.py

# You have to use the '["exec_location", "arg1", "arg2", ..., "argn"]' method so things exec properly.
# https://docs.docker.com/engine/reference/builder/#entrypoint
ENTRYPOINT ["aws_saml.py"]
