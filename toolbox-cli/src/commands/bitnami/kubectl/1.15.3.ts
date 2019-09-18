import {Command, flags} from '@oclif/command'
import {execute_docker, get_command_version} from '../../../helpers'

export default class RunKubectl extends Command {
  // Good tutorial on what we are doing here:
  //  https://blog.heroku.com/cli-flags-get-started-with-oclif
  //  https://zaiste.net/nodejs-child-process-spawn-exec-fork-async-await/

  static strict = false // Allow passing in sub-args to the docker container
  //static hidden = true // Prevent the oclif from showing it's help

  static description = `Launch kubectl ${get_command_version(__filename)} via an executable docker container.`

  static examples = [
    `$ kubectl get pods -A`,
    `$ kubectl get nodes -A`,
    `$ kubectl apply -k .`,
  ]

  async run() {
    const { argv } = this.parse()
    const command_version = get_command_version(__filename)
    const options = {
                      docker_args: [
                        "--cap-add IPC_LOCK",
                      ],
                      image_name: `bitnami/kubectl:${command_version}`
                    }

    await execute_docker(this, __filename, argv, options)
  }
}
