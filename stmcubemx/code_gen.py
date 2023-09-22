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

# Obtain the make database which is easier to parse for the needed parameters
make_database = subprocess.run(['make', '-nprR', '--directory=stmcubemx'], capture_output=True)

# Parse the database
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

# Generate meson.build file for the CubeMX auto generated code
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

    f.write("libstm = static_library('stm', stm_srcs, include_directories : stm_incs)\n\n")

    f.write("libstm_dep = declare_dependency(include_directories : stm_incs, link_with : libstm)\n\n")

    f.write("stm_c_args = [\n")
    for c_def in c_defs:
        f.write(f"  '{c_def}',\n")
    f.write(f"  '{cpu[0]}',\n")
    f.write(f"  '{float_abi[0]}',\n")
    f.write("  '-mabi=aapcs',\n")
    f.write("  '-mthumb']\n\n")

    f.write("stm_c_link_args = [\n")
    f.write(f"  '{cpu[0]}',\n")
    f.write(f"  '{float_abi[0]}',\n")
    f.write("  '-mabi=aapcs',\n")
    f.write("  '-mthumb']\n\n")

    f.write(f"ld_path = '{path.dirname(path.realpath(ldscript[0]))}/stmcubemx'\n")
    f.write(f"ld_filename = '{ldscript[0]}'\n")
    f.write('\n')

    f.write(f"cpu = '{cpu[0].split('=')[1]}'\n")
