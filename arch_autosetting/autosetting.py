from helepers import *
import time
import pprint

md_dict = read_code_from_md(_md='HowToSetup_Arch_SSH.md', code_start='~~~code', code_end='~~~',
                            command_letter='//', default_command='clip')


for number, section in enumerate(md_dict):
    is_valid_command(md_dict[section], number, _environment='arch')

time.sleep(2)


for i in md_dict[7]:
    run_command_arch(i)
    time.sleep(0.5)
