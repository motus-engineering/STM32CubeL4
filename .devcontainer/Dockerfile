# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.234.0/containers/ubuntu/.devcontainer/base.Dockerfile

# [Choice] Ubuntu version: ubuntu-22.04, ubuntu-20.04, ubuntu-18.04
ARG VARIANT="jammy"
FROM mcr.microsoft.com/devcontainers/base:${VARIANT}

# Install dependencies
RUN apt-get update && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get -y install --no-install-recommends build-essential \
                                               ninja-build \
                                               git \
                                               python3.11 \
                                               python3-pip \
                                               wget \
                                               libncurses5 \
                                               openjdk-19-jdk

# Install python dependencies
RUN pip install meson

# Google Drive file IDs of file to download
ARG STM32_CUBE_MX_INSTALLER_FILE_ID=1oPy8HTI8QHr0n1vqJy9iJ6M1EMlHL0KU
ARG STM32_CUBE_MX_AUTO_INSTALLER_FILE_ID=1m3WB_VqmxN13ZDQACiD_LrCSMh6JoISB

# Download script
COPY --chown=vscode:vscode --chmod=555 wget_drive.sh /home/vscode/temp/

# Download and install STM32CubeMX
RUN /home/vscode/temp/wget_drive.sh ${STM32_CUBE_MX_INSTALLER_FILE_ID} /home/vscode/temp/stm32cubemx.zip && \
    unzip /home/vscode/temp/stm32cubemx.zip -d /home/vscode/temp && \
    /home/vscode/temp/wget_drive.sh ${STM32_CUBE_MX_AUTO_INSTALLER_FILE_ID} /home/vscode/temp/stm32cubemx_auto-install.xml && \
    /home/vscode/temp/SetupSTM32CubeMX-6.9.2 /home/vscode/temp/stm32cubemx_auto-install.xml

# Clean up downloads
RUN rm -r /home/vscode/temp
