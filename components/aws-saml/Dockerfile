FROM toolbox_aws-cli:latest
USER root

# Ensure the executable is installed into $BIN_DIR (which is part of $PATH in the base toolbox image layer)
# Otherwise the container entrypoint doesn't work as intended :/
ENV BIN_DIR=${BIN_DIR:-"/usr/local/bin"}

RUN apk add --no-cache curl python3 groff && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
    cd /tmp/

RUN apk add --no-cache libxml2-dev py-lxml && \
    python -m pip install boto3 requests BeautifulSoup4 lxml configparser

ADD ./aws_saml.py ${BIN_DIR}/aws_saml.py
RUN chmod +x ${BIN_DIR}/aws_saml.py

# You have to use the '["exec_location", "arg1", "arg2", ..., "argn"]' method so things exec properly.
# https://docs.docker.com/engine/reference/builder/#entrypoint
ENTRYPOINT ["aws_saml.py"]
