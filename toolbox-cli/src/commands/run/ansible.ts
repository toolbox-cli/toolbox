import {Command, flags} from '@oclif/command'
import {execute_docker} from '../../helpers'

export default class RunAnsible extends Command {
  // Good tutorial on what we are doing here:
  //  https://blog.heroku.com/cli-flags-get-started-with-oclif
  //  https://zaiste.net/nodejs-child-process-spawn-exec-fork-async-await/

  static strict = false // Allow passing in sub-args to the docker container
  //static hidden = true // Prevent the oclif from showing it's help

  static description = `Launch ansible cli via an executable docker container.`

  static examples = [
    `$ toolbox run:ansible <host-pattern> [options]`,
    `$ toolbox run:ansible-playbook [options] playbook.yml [playbook2 ...]`,
    `$ toolbox run:ansible-vault [create|decrypt|edit|encrypt|encrypt_string|rekey|view] [options] [vaultfile.yml]`,
    `$ toolbox run:ansible-galaxy [delete|import|info|init|install|list|login|remove|search|setup] [--help] [options] ...`,
    `$ toolbox run:ansible-console [<host-pattern>] [options]`,
    `$ toolbox run:ansible-config [view|dump|list] [--help] [options] [ansible.cfg]`,
    `$ toolbox run:ansible-doc [-l|-s] [options] [-t <plugin type] [plugin]`,
    `$ toolbox run:ansible-inventory [options] [host|group]`,
    `$ toolbox run:ansible-pull -U <repository> [options] [<playbook.yml>]`,
  ]

  static aliases = [
    `run:ansible-playbook`,
    `run:ansible-vault`,
    `run:ansible-galaxy`,
    `run:ansible-console`,
    `run:ansible-config`,
    `run:ansible-doc`,
    `run:ansible-inventory`,
    `run:ansible-pull`,
  ]

  async run() {
    const {argv} = this.parse()
    const extra_docker_args = ["--cap-add IPC_LOCK"]

    await execute_docker(this, __filename, argv, extra_docker_args)
  }
}
