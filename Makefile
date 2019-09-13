REPO_NAME  ?= toolbox
NAME       := devops/${REPO_NAME}
VERSION    := 0.0.1
CLI_PATH   := ./toolbox-cli

.PHONY: all
all: build tag npm-link
	#make npm-package

.PHONY: check_vars
check_vars:
	@test $(NAME)
	@test $(VERSION)

.PHONY: build
build: install-dependencies
	make check_vars
	NAME="$(NAME)" VERSION="$(VERSION)" docker-compose build --compress

.ONESHELL:
.PHONY: npm-link
npm-link: build
	make check_vars
	rm -rf ./node-modules
	@echo "Updating the version tag for the npm cli package"
	sed -i '' "0,/\"version\": \".*\"/s//\"version\": \"${VERSION}\"/" ${CLI_PATH}/package.json

	@echo "Linking the 'toolbox-cli' to '/usr/bin/toolbox'"
	pwd
	npm install ${CLI_PATH}
	sudo npm link ${CLI_PATH}

.ONESHELL:
package: install-dependencies
	cd toolbox-cli
	npm install
	oclif-dev pack
	# Todo: Upload the archives somewhere...

.PHONY: tag
tag: build
	make check_vars
	@./tag.sh "$(NAME)" "$(VERSION)" "${REPO_NAME}"

.PHONY: push
push: build
	make check_vars
	@./push.sh "$(NAME)" "$(VERSION)"

install-dependencies:
	# Install node: https://github.com/nodesource/distributions/blob/master/README.md
	@which npm || sudo yum install -y npm p7zip p7zip-plugins || \
								sudo apt-get install -y npm p7zip-full
	@which oclif || sudo npm install -g oclif
	@which oclif-dev || sudo npm install -g @oclif/dev-cli
	@which pkg || sudo npm install -g pkg