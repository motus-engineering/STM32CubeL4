project('stm32l4', 'c', 'cpp',
  meson_version: '>=1.2.0',
  version: '1.18.0',
)

# run cubemx
message('Generating STM32CubeMX files.')
cubemx_gen = run_command('/home/vscode/STM32CubeMX/STM32CubeMX', '-q', '/workspaces/STM32CubeL4/stmcubemx/cube_mx_script.txt', check: true)

# autogen meson.build file
message('Generating meson files.')
meson_gen = run_command('python3', 'stmcubemx/code_gen.py', check: true)

# now add the meson.build file for the project
subdir('stmcubemx')
