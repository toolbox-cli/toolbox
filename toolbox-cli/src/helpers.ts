import {Command} from '@oclif/command'
const { spawn } = require('child_process');

export async function execute_docker(context: Command,
                                      filepath: string,
                                      argv: Array<string>,
                                      options: {
                                        docker_args?: string[];
                                        image_name?: string;
                                      }
                                    ) {

    var util = require('util');
    var name_fields = extract_name_fields_from_path(filepath)
    if (context.config.debug) {
      console.log(`command_type: ${name_fields.command_type} command_name: ${name_fields.command_name} command_version: ${name_fields.command_version}`)
    }
    options.image_name = get_image_name(context, filepath, argv, options)

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
    const command_process = spawn(`${command_full}`, {
                              cwd: process.cwd(),
                              detached: true,
                              shell: true,
                              stdio: 'inherit'
                            }
    )

    command_process.on('error', () => {
      console.error('Failed to start subprocess.');
    });

    command_process.on('close', (code: number) => {
      if (code !== 0 && context.config.debug) {
        console.log(`[!] '${name_fields.command_name}' exited with code ${code}`);
      }

      if (code == 125) {
        console.log(`Is the Docker engine installed and running?`)
      }
    });
}
export function get_image_name(context: Command,
                                filepath: string,
                                argv: Array<string>,
                                options: {
                                  docker_args?: string[];
                                  image_name?: string;
                                }
                              ) {

  var command_config = extract_command_config(filepath)
  var name_fields = extract_name_fields_from_path(filepath)
  var image_name = options.image_name
  if (context.config.debug) {
    console.log(`command_type: ${name_fields.command_type} command_name: ${name_fields.command_name} command_version: ${name_fields.command_version}`)
  }

  // If the image name is passed in, let's use that as the ultimate source of truth
  if (image_name) {
    return image_name
  }

  // Let's use the dockerhub naming pattern (you cannot have multiple folders)
  try {
    if (command_config.docker_registry) {
      image_name = `${command_config.docker_registry}:${name_fields.command_type}_${name_fields.command_name}_${name_fields.command_version}`
      return image_name
    }
  }
  catch (e) {
    if (context.config.debug) {
      console.log(`The command '${name_fields.command_name}' does not have a docker registry defined in 'toolbox.json'`)
    }
  }

  // Let's use the dockerhub naming pattern LOCALLY (you cannot have multiple folders)
  image_name = `${name_fields.command_type}_${name_fields.command_name}_${name_fields.command_version}`
  return image_name
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

export function normalized_toolbox_config() {
  var normalizeData = require('normalize-package-data')
  var packageData = require("../toolbox.json")
  normalizeData(packageData)
  var json_string = JSON.stringify(packageData)
  return JSON.parse(json_string)
}

export function extract_command_config(filepath: string) {
  try {
    var name_fields = extract_name_fields_from_path(filepath)
    var command_config = normalized_toolbox_config()["commands"][`${name_fields.command_type}`][`${name_fields.command_name}`]
    return command_config
  }
  catch (e) {
    return ""
  }
}