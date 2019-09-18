import {Command, flags} from '@oclif/command'
import {execute_docker, get_command_version} from '../../../helpers'

export default class RunTerraform extends Command {
  // Good tutorial on what we are doing here:
  //  https://blog.heroku.com/cli-flags-get-started-with-oclif
  //  https://zaiste.net/nodejs-child-process-spawn-exec-fork-async-await/

  static strict = false // Allow passing in sub-args to the docker container
  //static hidden = true // Prevent the oclif from showing it's help

  static description = `Launch Terraform ${get_command_version(__filename)} via an executable docker container.`

  static examples = [
    `$ toolbox run:terraform refresh`,
    `$ toolbox run:terraform plan`,
    `$ toolbox run:terraform apply`,
  ]

  async run() {
    const { argv } = this.parse()
    const command_version = get_command_version(__filename)
    const options = {
                      docker_args: [
                        "--cap-add IPC_LOCK",
                      ],
                      image_name: `hashicorp/terraform:${command_version}`
                    }

    await execute_docker(this, __filename, argv, options)
  }
}
