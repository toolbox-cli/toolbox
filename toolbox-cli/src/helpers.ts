import {Command} from '@oclif/command'

export async function execute_docker(context: Command,
                                      filepath: string,
                                      argv: Array<string>,
                                      options: {
                                        docker_args?: string[];
                                        image_name?: string;
                                      }
                                    ) {

    var util = require('util');
    var spawn = util.promisify(require('child_process').spawn);
    var version = context.config.pjson.version
    var name_fields = extract_name_fields_from_path(filepath)
    console.log(`command_type: ${name_fields.command_type} command_name: ${name_fields.command_name} command_version: ${name_fields.command_version}`)

    // No custom docker image path provided; generate a relative one to our repos
  if (!options.image_name) {
      options.image_name = `devops/toolbox/${name_fields.command_name}:${name_fields.command_version}`
      console.log(`${options.image_name}`)
    }

    // If no custom extra docker_args, just set it to empty
    if (!options.docker_args) {
      options.docker_args = []
    }

    var command_full = `
                        docker run ${options.docker_args.join(" ")} \
                            --rm \
                            -it \
                            -v ${process.cwd()}:${process.cwd()} \
                            -v ${context.config.home}:/root \
                            -v ${context.config.home}:${context.config.home} \
                            -w ${process.cwd()} \
                            ${options.image_name} \
                            ${argv.join(" ")}
                      `

    if (context.config.debug) {
      console.log(`\n` +
                  `➜ ${command_full.toString().replace(/\s+/g,' ')}` +
                  `\n`)
    }

    // Spawn the docker command.
    spawn(`${command_full}`, {
                              cwd: process.cwd(),
                              detached: true,
                              shell: true,
                              stdio: 'inherit'
                            }
    );
}

export function extract_name_fields_from_path(filepath: string) {
  var command_version = require('path').basename(filepath).split(".ts")[0].split(".js")[0]; // Remove extensions from name.
  var command_name = require('path').basename(require('path').dirname(filepath))
  var command_type = require('path').basename(require('path').dirname(require('path').dirname(filepath)))

  var name_fields = {
    command_version: command_version,
    command_name: command_name,
    command_type: command_type
  }

  return name_fields
}

export function get_command_type(filepath: string) {
  return extract_name_fields_from_path(filepath).command_type
}
export function get_command_name(filepath: string) {
  return extract_name_fields_from_path(filepath).command_name
}
export function get_command_version(filepath: string) {
  return extract_name_fields_from_path(filepath).command_version
}