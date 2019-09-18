FROM toolbox_vagrant:latest
USER root

# Ensure the executable is installed into $BIN_DIR (which is part of $PATH in the base toolbox image layer)
# Otherwise the container entrypoint doesn't work as intended :/
ENV BIN_DIR=${BIN_DIR:-"/usr/local/bin"}
ENV PACKER_VERSION=${PACKER_VERSION:-"1.4.2"}
ENV ARCH=${ARCH:-"amd64"}

ADD ./packer_${PACKER_VERSION}_linux_${ARCH}.zip /root/

RUN unzip /root/packer_${PACKER_VERSION}_linux_${ARCH}.zip -d ${BIN_DIR} && \
    chmod +x ${BIN_DIR}/packer

# You have to use the '["exec_location", "arg1", "arg2", ..., "argn"]' method so things exec properly.
# https://docs.docker.com/engine/reference/builder/#entrypoint
ENTRYPOINT ["packer"]