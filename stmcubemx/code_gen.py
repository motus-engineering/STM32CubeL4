'''
This script should run anytime the Makefile is changed to regenerate the
meson.build file for the cubeMX generated code
'''

import re
from os import path
import subprocess

# Initialize variables to store extracted information
target = []
c_sources_subproject = []
c_includes_subproject = []
asm_source = []
c_defs = []
ldscript = []
cpu = []
fpu = []
float_abi = []

# Define a dictionary to map regex patterns to variables
pattern_variable_mapping = {
    'TARGET': target,
    'C_SOURCES': c_sources_subproject,
    'C_INCLUDES': c_includes_subproject,
    'ASM_SOURCES': asm_source,
    'C_DEFS': c_defs,
    'LDSCRIPT': ldscript,
    'CPU': cpu,
    'FPU': fpu,
    'FLOAT-ABI': float_abi,
}

#TODO handle the stm32l4 subfolder more generically
make_database = subprocess.run(['make', '-nprR', '--directory=stmcubemx'], capture_output=True)

for line in make_database.stdout.decode().splitlines():
    for pattern, variable in pattern_variable_mapping.items():
        m = re.match(pattern, line)
        if m:
            parts = m.string.split()[2:]
            if pattern == 'C_SOURCES':
                for part in parts:
                    if path.isabs(part):
                        variable.append(path.join('..', path.relpath(part)))
                    else:
                        variable.append(part)
            elif pattern == 'C_INCLUDES':
                for part in parts:
                    part = part.removeprefix('-I')
                    if path.isabs(part):
                        variable.append(path.join('..', path.relpath(part)))
                    else:
                        variable.append(part)
            else:
                variable.extend([part for part in parts])

# Generate meson.build file for Auto Generated Code App code
with open(path.join('stmcubemx', 'meson.build'), 'w', encoding='utf-8') as f:
    f.write('# Auto Generated File\n\n')

    f.write('stm_incs = [include_directories(')
    for c_include in c_includes_subproject:
        f.write(f"'{c_include}',\n")
    f.write(')]\n\n')

    f.write('stm_srcs = files(')
    for c_source in c_sources_subproject:
        f.write(f"'{c_source}',\n")
    f.write(')\n\n')

    f.write(f"stm_srcs += files('{asm_source[0]}')\n\n")

# Generate cross compile file for specific target
with open(path.join('stmcubemx', target[0] + '.ini'), 'w', encoding='utf-8') as f:
    preamble = '''# Auto Generated File

# Meson Cross-compilation File
# This file should be layered after arm.ini
# Requires that arm-none-eabi-* is found in your PATH
# For more information: http://mesonbuild.com/Cross-compilation.html

'''
    f.write(preamble)

    f.write('[built-in options]\n')
    f.write("c_args = [\n")
    for c_def in c_defs:
        f.write(f"  '{c_def}',\n")
    f.write(f"  '{cpu[0]}',\n")
    f.write(f"  '{float_abi[0]}',\n")
    f.write("  '-mabi=aapcs',\n")
    f.write("  '-mthumb']\n\n")

    f.write("c_link_args = [\n")
    f.write(f"  '{cpu[0]}',\n")
    f.write(f"  '{float_abi[0]}',\n")
    f.write("  '-mabi=aapcs',\n")
    f.write("  '-mthumb']\n\n")

    f.write('[properties]\n')
    f.write(f"ld_path = 'stmcubemx/{target[0]}'\n")
    f.write(f"ld_filename = '{ldscript[0]}'\n")
    f.write('\n')

    f.write('[host_machine]\n')
    f.write(f"cpu = '{cpu[0].split('=')[1]}'\n")
    f.write('\n')
