# Project for providing the STM32 library code.
# It is expected to be used as a subproject inside another meson project.
project('stm32l4', 'c', 'cpp',
  meson_version: '>=1.2.0',
  version: '1.18.0',
)

# Build CubeMX script
message('Generating STM32CubeMX files.')
cube_mx_script_file = meson.project_source_root() / 'stmcubemx/cube_mx_script.txt'
ioc_file = meson.project_source_root() / 'stmcubemx/stm32l476rgtx.ioc'
script_gen = run_command('python3',
  meson.project_source_root() / 'stmcubemx/cube_mx_script_gen.py',
  cube_mx_script_file,
  ioc_file,
  check: true)

# Run CubeMX to generate project files
cubemx_gen = run_command('/home/vscode/STM32CubeMX/STM32CubeMX', '-q', cube_mx_script_file, check: true)

# Generate meson.build file based on the Makefile created by CubeMX
message('Generating meson files.')
meson_gen = run_command('python3', 'stmcubemx/code_gen.py', check: true)

# Now add the generated meson.build file for the (sub)project
subdir('stmcubemx')
