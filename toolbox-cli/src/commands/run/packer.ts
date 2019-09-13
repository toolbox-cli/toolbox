import {Command, flags} from '@oclif/command'
import {execute_docker} from '../../helpers'

export default class RunPacker extends Command {
  // Good tutorial on what we are doing here:
  //  https://blog.heroku.com/cli-flags-get-started-with-oclif
  //  https://zaiste.net/nodejs-child-process-spawn-exec-fork-async-await/

  static strict = false // Allow passing in sub-args to the docker container
  //static hidden = true // Prevent the oclif from showing it's help

  static description = `Launch Packer via an executable docker container.`

  static examples = [
    `$ toolbox run:packer validate ./my-image.json`,
    `$ toolbox run:packer build ./my-image.json`,
  ]

  async run() {
    const {argv} = this.parse()
    const extra_docker_args = ["--cap-add IPC_LOCK"]

    await execute_docker(this, __filename, argv, extra_docker_args)
  }
}
