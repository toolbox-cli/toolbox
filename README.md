## toolbox cli
A growing list of apps and tools that can be used across platforms.

## Goals
* The ```toolbox``` cli utility is a wrapper that executes versioned docker images.
* The ```toolbox``` cli utility runs on any operation system and can be used in pipelines and scripts.
* The ```toolbox``` cli utility allows for our DevOps team to ensure that the company is running with unified tools.
* The ```toolbox``` cli utility can allow us to package full GUI based application as well ([1](https://github.com/fgrehm/docker-eclipse), [2](https://dev.to/darksmile92/run-gui-app-in-linux-docker-container-on-windows-host-4kde), [3](https://www.infoworld.com/article/3329536/microsoft-puts-desktop-apps-in-containers-with-windows-sandbox.html)).

## For our customers...
Hello developers!

I have created a CLI utility to centrally manage and distribute common tools and utilities that are used by our employees.
It’s basically a wrapper around various immutable/versioned docker images which will provide our developers and engineers a suite of tools that they can use across their development platforms (linux, windows, mac).

The CLI utility currently has the following components: aws-cli, aws saml script, terraform, packer, and ansible.
In the future we can add correct versions of java, node, python, and other bundles which employees would find useful. It’s a really nice way to package and promote the use of a unified suite of tools.

## Structure
* ./Makefile -- triggers the build steps. It creates versioned images and creates an NPM module which executes the versioned docker images.
* /cli-command-images -- Contains the dockerfiles for creating the images
* /toolbox-cli - the NPM based module which leverages the oclif framework for generating the CLI.
    * The toolbox CLI is composed oclif "commands". Commands are hierarchically separated by folder names. The top level folder is ```./toolbox-cli/src/commands```
    * Within the `commands` directory, there are sub-directories which specify the command in the following manner:
        * ```./commands/{TYPE}/{NAME}/{VERSION}```
            Examples:

                ./commands/hashicorp/terraform/0.11.13
                ./commands/hashicorp/terraform/0.11.14
                ./commands/hashicorp/packer/1.4.3
                ./commands/aws/aws-cli/0.0.1
                ./commands/aws/aws-saml/0.0.1

    * The commands are evoked by using the `toolbox` command:
        Examples:

          ➜  toolbox aws:aws-saml:0.0.1 -i adfs.mywork.net -u josh.giron@mywork.net -r eu-west-1
          ➜  toolbox aws:aws-cli:0.0.1 ec2 describe-instances
          ➜  toolbox hashicorp:terraform:0.11.13 init
          ➜  toolbox hashicorp:terraform:0.11.13 destroy
          ➜  toolbox hashicorp:terraform:0.11.13 apply
          ➜  toolbox ide:eclipse:4.4.1 &
          ^ (This is sent to the background because it is a full GUI based app)
## Announcement
I am proud to announce the addition of a new software utility to aid you with cloud development and your company's DevOps journey. This new toolkit is called the “toolbox-cli” (toolbox command line interface).

It’s main purpose is for pre-packaging commonly used tools and software so that developers, and your DevOps processes, have a consistent experience across all teams and environments. The toolbox cli executes versioned and immutable Docker Containers for the operations. This means that as long as you have docker installed on your machine, the toolbox will work as expected across MacOS, Linux, and Windows!

We plan to add new tooling such as build tools, debugging tools, deployment tools, and integrated development environments so that teams can be more effective and not have to worry about managing so many things. The Toolbox CLI will allow you to define team specific Docker container commands in the future as well; so, stay tuned!

## Current toolbox commands
[Toolbox CLI Commands](https://github.com/toolbox-cli/toolbox/blob/develop/toolbox-cli/README.md#commands)

## Usage
Below are the general usage details:
```bash
➜  toolbox run:aws-saml --environment dev-example --role Administrator --no-ssl-verify
Username (@example.com email):
josh.giron
Password:


----------------------------------------------------------------
Your new access key pair has been stored in the AWS configuration file ~/.aws/credentials under the default profile.
Note that it will expire at 2019-07-29 19:51:04+00:00.
After this time, you may safely rerun this script to refresh your access key pair.
To use this credential, call the AWS CLI with the --profile option (e.g. aws --profile default ec2 describe-instances).
----------------------------------------------------------------


➜  toolbox run:aws-cli cloudformation list-stacks
{
    "StackSummaries": [
        {
            "StackId": "arn:aws:cloudformation:us-east-1:012345678901:stack/toolbox/b152db20-b217-11e9-a3e4-126514929126",
            "StackName": "toolbox",
            "TemplateDescription": "Stack for r53 recordset, target group, listener, ecs service, task def.\n",
            "CreationTime": "2019-07-29T15:44:04.082Z",
            "StackStatus": "CREATE_COMPLETE",
           "DriftInformation": {
                "StackDriftStatus": "NOT_CHECKED"
            }
        },
…
…

➜  toolbox aws:aws-saml:0.0.1 -i adfs.mywork.net -u josh.giron@mywork.net -r eu-west-1
➜  toolbox aws:aws-cli:0.0.1 ec2 describe-instances
➜  toolbox hashicorp:terraform:0.11.13 init
➜  toolbox hashicorp:terraform:0.11.13 destroy
➜  toolbox hashicorp:terraform:0.11.13 apply
```

The Toolbox CLI is now internally available and we would love immediate feedback!

Please feel free to download and install the new tool by reading the installation details at:
[installation.md](/toolbox-cli/installation.md)
