'''
This Python script creates the CubeMX script that is used to generate the STM32
library for the project.
'''

from sys import argv

cube_mx_script_path = argv[1]
cube_mx_ioc_path = argv[2]

# See the STM32CubeMX manual for information on the script commands
with open(cube_mx_script_path, 'w', encoding='utf-8') as f:
    f.write(f'config load {cube_mx_ioc_path}\n')
    f.write('project generate\n')
    f.write('exit\n')
