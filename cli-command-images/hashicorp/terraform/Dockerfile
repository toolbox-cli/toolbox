FROM toolbox_base:latest
USER root

# Ensure the executable is installed into $BIN_DIR (which is part of $PATH in the base toolbox image layer)
# Otherwise the container entrypoint doesn't work as intended :/
ENV BIN_DIR=${BIN_DIR:-"/usr/local/bin"}
ENV TERRAFORM_VERSION=${TERRAFORM_VERSION:-"0.12.6"}
ENV ARCH=${ARCH:-"amd64"}

# What's going on here?
# - Download the indicated release along with its checksums and signature for the checksums
# - Extract the zip file so it can be run
#
# https://github.com/hashicorp/terraform/blob/master/scripts/docker-release/Dockerfile-release

COPY terraform_${TERRAFORM_VERSION}_linux_${ARCH}.zip .

RUN echo "Building image for Terraform ${TERRAFORM_VERSION} to ${BIN_DIR}/" && \
    unzip terraform_${TERRAFORM_VERSION}_linux_${ARCH}.zip -d ${BIN_DIR}/ && \
    rm -f terraform_${TERRAFORM_VERSION}_linux_${ARCH}.zip

# You have to use the '["exec_location", "arg1", "arg2", ..., "argn"]' method so things exec properly.
# https://docs.docker.com/engine/reference/builder/#entrypoint
ENTRYPOINT ${BIN_DIR}/terraform