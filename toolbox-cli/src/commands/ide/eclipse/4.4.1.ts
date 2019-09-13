import {Command, flags} from '@oclif/command'
import {execute_docker, get_command_version} from '../../../helpers'

export default class IdeEclipse extends Command {
  // Good tutorial on what we are doing here:
  //  https://blog.heroku.com/cli-flags-get-started-with-oclif
  //  https://zaiste.net/nodejs-child-process-spawn-exec-fork-async-await/

  static strict = false // Allow passing in sub-args to the docker container
  //static hidden = true // Prevent the oclif from showing it's help

  static description = `Launch the Eclipse ${get_command_version(__filename)} IDE via an executable docker container.`

  async run() {
    const { argv } = this.parse()
    const command_version = get_command_version(__filename)
    const options = {
                      docker_args: [
                        "--cap-add IPC_LOCK",
                        "-e DISPLAY=$DISPLAY",
                        "-v /tmp/.X11-unix:/tmp/.X11-unix",
                      ],
                      image_name: `fgrehm/eclipse:v${command_version}`
                    }

    execute_docker(this, __filename, argv, options)
  }
}
