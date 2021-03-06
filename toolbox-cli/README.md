toolbox
=======

cli for running a growing list of containerized apps and tools.

[![oclif](https://img.shields.io/badge/cli-oclif-brightgreen.svg)](https://oclif.io)
[![Version](https://img.shields.io/npm/v/toolbox.svg)](https://npmjs.org/package/toolbox)
[![Downloads/week](https://img.shields.io/npm/dw/toolbox.svg)](https://npmjs.org/package/toolbox)
[![License](https://img.shields.io/npm/l/toolbox.svg)](https://github.com/n0rig/toolbox/blob/master/package.json)

<!-- toc -->
* [Usage](#usage)
* [Commands](#commands)
<!-- tocstop -->
# Usage
<!-- usage -->
```sh-session
$ npm install -g @toolbox-cli/toolbox
$ toolbox COMMAND
running command...
$ toolbox (-v|--version|version)
@toolbox-cli/toolbox/0.0.3 darwin-x64 node-v12.10.0
$ toolbox --help [COMMAND]
USAGE
  $ toolbox COMMAND
...
```
<!-- usagestop -->
# Commands
<!-- commands -->
* [`toolbox autocomplete [SHELL]`](#toolbox-autocomplete-shell)
* [`toolbox aws:aws-cli:0.0.1`](#toolbox-awsaws-cli001)
* [`toolbox aws:aws-saml:0.0.1`](#toolbox-awsaws-saml001)
* [`toolbox commands`](#toolbox-commands)
* [`toolbox hashicorp:ansible:0.0.1`](#toolbox-hashicorpansible001)
* [`toolbox hashicorp:packer:1.4.3`](#toolbox-hashicorppacker143)
* [`toolbox hashicorp:terraform:0.11.13`](#toolbox-hashicorpterraform01113)
* [`toolbox hashicorp:terraform:0.12.6`](#toolbox-hashicorpterraform0126)
* [`toolbox help [COMMAND]`](#toolbox-help-command)
* [`toolbox ide:eclipse:4.4.1`](#toolbox-ideeclipse441)
* [`toolbox plugins`](#toolbox-plugins)
* [`toolbox plugins:install PLUGIN...`](#toolbox-pluginsinstall-plugin)
* [`toolbox plugins:link PLUGIN`](#toolbox-pluginslink-plugin)
* [`toolbox plugins:uninstall PLUGIN...`](#toolbox-pluginsuninstall-plugin)
* [`toolbox plugins:update`](#toolbox-pluginsupdate)
* [`toolbox update [CHANNEL]`](#toolbox-update-channel)

## `toolbox autocomplete [SHELL]`

display autocomplete installation instructions

```
USAGE
  $ toolbox autocomplete [SHELL]

ARGUMENTS
  SHELL  shell type

OPTIONS
  -r, --refresh-cache  Refresh cache (ignores displaying instructions)

EXAMPLES
  $ toolbox autocomplete
  $ toolbox autocomplete bash
  $ toolbox autocomplete zsh
  $ toolbox autocomplete --refresh-cache
```

_See code: [@oclif/plugin-autocomplete](https://github.com/oclif/plugin-autocomplete/blob/v0.1.4/src/commands/autocomplete/index.ts)_

## `toolbox aws:aws-cli:0.0.1`

Launch the AWS cli via an executable docker container.

```
USAGE
  $ toolbox aws:aws-cli:0.0.1

EXAMPLES
  $ toolbox run:aws-cli iam list-instance-profiles --no-verify-ssl
  $ toolbox run:aws-cli cloudformation list-stacks
```

_See code: [src/commands/aws/aws-cli/0.0.1.ts](https://github.com/toolbox-cli/toolbox/blob/v0.0.3/src/commands/aws/aws-cli/0.0.1.ts)_

## `toolbox aws:aws-saml:0.0.1`

Launch AWS SAML login script via an executable docker container.

```
USAGE
  $ toolbox aws:aws-saml:0.0.1

EXAMPLE
  $ toolbox run:aws-saml --environment=dev-example --role=Administrator  --profile=default --no-verify-ssl
```

_See code: [src/commands/aws/aws-saml/0.0.1.ts](https://github.com/toolbox-cli/toolbox/blob/v0.0.3/src/commands/aws/aws-saml/0.0.1.ts)_

## `toolbox commands`

list all the commands

```
USAGE
  $ toolbox commands

OPTIONS
  -h, --help  show CLI help
  -j, --json  output in json format
  --hidden    also show hidden commands
```

_See code: [@oclif/plugin-commands](https://github.com/oclif/plugin-commands/blob/v1.2.3/src/commands/commands.ts)_

## `toolbox hashicorp:ansible:0.0.1`

Launch ansible 2.8.3 cli via an executable docker container.

```
USAGE
  $ toolbox hashicorp:ansible:0.0.1

ALIASES
  $ toolbox run:ansible-playbook
  $ toolbox run:ansible-vault
  $ toolbox run:ansible-galaxy
  $ toolbox run:ansible-console
  $ toolbox run:ansible-config
  $ toolbox run:ansible-doc
  $ toolbox run:ansible-inventory
  $ toolbox run:ansible-pull

EXAMPLES
  $ toolbox run:ansible <host-pattern> [options]
  $ toolbox run:ansible-playbook [options] playbook.yml [playbook2 ...]
  $ toolbox run:ansible-vault [create|decrypt|edit|encrypt|encrypt_string|rekey|view] [options] [vaultfile.yml]
  $ toolbox run:ansible-galaxy [delete|import|info|init|install|list|login|remove|search|setup] [--help] [options] ...
  $ toolbox run:ansible-console [<host-pattern>] [options]
  $ toolbox run:ansible-config [view|dump|list] [--help] [options] [ansible.cfg]
  $ toolbox run:ansible-doc [-l|-s] [options] [-t <plugin type] [plugin]
  $ toolbox run:ansible-inventory [options] [host|group]
  $ toolbox run:ansible-pull -U <repository> [options] [<playbook.yml>]
```

_See code: [src/commands/hashicorp/ansible/0.0.1.ts](https://github.com/toolbox-cli/toolbox/blob/v0.0.3/src/commands/hashicorp/ansible/0.0.1.ts)_

## `toolbox hashicorp:packer:1.4.3`

Launch Packer 1.4.3 via an executable docker container.

```
USAGE
  $ toolbox hashicorp:packer:1.4.3

EXAMPLES
  $ toolbox run:packer validate ./my-image.json
  $ toolbox run:packer build ./my-image.json
```

_See code: [src/commands/hashicorp/packer/1.4.3.ts](https://github.com/toolbox-cli/toolbox/blob/v0.0.3/src/commands/hashicorp/packer/1.4.3.ts)_

## `toolbox hashicorp:terraform:0.11.13`

Launch Terraform 0.11.13 via an executable docker container.

```
USAGE
  $ toolbox hashicorp:terraform:0.11.13

EXAMPLES
  $ toolbox run:terraform refresh
  $ toolbox run:terraform plan
  $ toolbox run:terraform apply
```

_See code: [src/commands/hashicorp/terraform/0.11.13.ts](https://github.com/toolbox-cli/toolbox/blob/v0.0.3/src/commands/hashicorp/terraform/0.11.13.ts)_

## `toolbox hashicorp:terraform:0.12.6`

Launch Terraform 0.12.6 via an executable docker container.

```
USAGE
  $ toolbox hashicorp:terraform:0.12.6

EXAMPLES
  $ toolbox run:terraform refresh
  $ toolbox run:terraform plan
  $ toolbox run:terraform apply
```

_See code: [src/commands/hashicorp/terraform/0.12.6.ts](https://github.com/toolbox-cli/toolbox/blob/v0.0.3/src/commands/hashicorp/terraform/0.12.6.ts)_

## `toolbox help [COMMAND]`

display help for toolbox

```
USAGE
  $ toolbox help [COMMAND]

ARGUMENTS
  COMMAND  command to show help for

OPTIONS
  --all  see all commands in CLI
```

_See code: [@oclif/plugin-help](https://github.com/oclif/plugin-help/blob/v2.2.1/src/commands/help.ts)_

## `toolbox ide:eclipse:4.4.1`

Launch the Eclipse 4.4.1 IDE via an executable docker container.

```
USAGE
  $ toolbox ide:eclipse:4.4.1
```

_See code: [src/commands/ide/eclipse/4.4.1.ts](https://github.com/toolbox-cli/toolbox/blob/v0.0.3/src/commands/ide/eclipse/4.4.1.ts)_

## `toolbox plugins`

list installed plugins

```
USAGE
  $ toolbox plugins

OPTIONS
  --core  show core plugins

EXAMPLE
  $ toolbox plugins
```

_See code: [@oclif/plugin-plugins](https://github.com/oclif/plugin-plugins/blob/v1.7.8/src/commands/plugins/index.ts)_

## `toolbox plugins:install PLUGIN...`

installs a plugin into the CLI

```
USAGE
  $ toolbox plugins:install PLUGIN...

ARGUMENTS
  PLUGIN  plugin to install

OPTIONS
  -f, --force    yarn install with force flag
  -h, --help     show CLI help
  -v, --verbose

DESCRIPTION
  Can be installed from npm or a git url.

  Installation of a user-installed plugin will override a core plugin.

  e.g. If you have a core plugin that has a 'hello' command, installing a user-installed plugin with a 'hello' command 
  will override the core plugin implementation. This is useful if a user needs to update core plugin functionality in 
  the CLI without the need to patch and update the whole CLI.

ALIASES
  $ toolbox plugins:add

EXAMPLES
  $ toolbox plugins:install myplugin 
  $ toolbox plugins:install https://github.com/someuser/someplugin
  $ toolbox plugins:install someuser/someplugin
```

_See code: [@oclif/plugin-plugins](https://github.com/oclif/plugin-plugins/blob/v1.7.8/src/commands/plugins/install.ts)_

## `toolbox plugins:link PLUGIN`

links a plugin into the CLI for development

```
USAGE
  $ toolbox plugins:link PLUGIN

ARGUMENTS
  PATH  [default: .] path to plugin

OPTIONS
  -h, --help     show CLI help
  -v, --verbose

DESCRIPTION
  Installation of a linked plugin will override a user-installed or core plugin.

  e.g. If you have a user-installed or core plugin that has a 'hello' command, installing a linked plugin with a 'hello' 
  command will override the user-installed or core plugin implementation. This is useful for development work.

EXAMPLE
  $ toolbox plugins:link myplugin
```

_See code: [@oclif/plugin-plugins](https://github.com/oclif/plugin-plugins/blob/v1.7.8/src/commands/plugins/link.ts)_

## `toolbox plugins:uninstall PLUGIN...`

removes a plugin from the CLI

```
USAGE
  $ toolbox plugins:uninstall PLUGIN...

ARGUMENTS
  PLUGIN  plugin to uninstall

OPTIONS
  -h, --help     show CLI help
  -v, --verbose

ALIASES
  $ toolbox plugins:unlink
  $ toolbox plugins:remove
```

_See code: [@oclif/plugin-plugins](https://github.com/oclif/plugin-plugins/blob/v1.7.8/src/commands/plugins/uninstall.ts)_

## `toolbox plugins:update`

update installed plugins

```
USAGE
  $ toolbox plugins:update

OPTIONS
  -h, --help     show CLI help
  -v, --verbose
```

_See code: [@oclif/plugin-plugins](https://github.com/oclif/plugin-plugins/blob/v1.7.8/src/commands/plugins/update.ts)_

## `toolbox update [CHANNEL]`

update the toolbox CLI

```
USAGE
  $ toolbox update [CHANNEL]
```

_See code: [@oclif/plugin-update](https://github.com/oclif/plugin-update/blob/v1.3.9/src/commands/update.ts)_
<!-- commandsstop -->
