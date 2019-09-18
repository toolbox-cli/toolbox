REPO_NAME  ?= $(shell jq -r ".docker_registry" toolbox-cli/toolbox.json)
VERSION    := 0.0.1
CLI_PATH   := ./toolbox-cli

.PHONY: all
all: build tag npm-link
	#make npm-package

.PHONY: check_vars
check_vars:
	@test $(REPO_NAME)
	@test $(VERSION)

.PHONY: build
build: install-dependencies
	make check_vars
	VERSION="$(VERSION)" docker-compose build --compress

.ONESHELL:
npm-link: build
	make check_vars
	rm -rf ./node-modules
	@echo "Updating the version tag for the npm cli package"
	sed -i '' "0,/\"version\": \".*\"/s//\"version\": \"${VERSION}\"/" ${CLI_PATH}/package.json

	@echo "Linking the 'toolbox-cli' to '/usr/bin/toolbox'"
	pwd
	npm install ${CLI_PATH}
	sudo npm link ${CLI_PATH}

.PHONY: tag
tag: build
	make check_vars
	@./tag.sh "$(REPO_NAME)" "$(VERSION)"

.PHONY: push
push: build
	make check_vars
	@./push.sh "$(REPO_NAME)" "$(VERSION)"

.ONESHELL:
toolbox-patch-release: install-dependencies
	cd toolbox-cli; \
	pwd; \
	npx release-it -- patch --ci

.ONESHELL:
toolbox-minor-release: install-dependencies
	cd toolbox-cli; \
	pwd; \
	npx release-it -- minor --ci

.ONESHELL:
toolbox-major-release: install-dependencies
	cd toolbox-cli; \
	pwd; \
	npx release-it -- major --ci

install-dependencies:
	# Install node: https://github.com/nodesource/distributions/blob/master/README.md
	@which npm || sudo yum install -y npm p7zip p7zip-plugins || \
								sudo apt-get install -y npm p7zip-full
	@which oclif || sudo npm install -g oclif
	@which oclif-dev || sudo npm install -g @oclif/dev-cli
	@which pkg || sudo npm install -g pkg