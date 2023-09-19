# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.234.0/containers/ubuntu/.devcontainer/base.Dockerfile

# [Choice] Ubuntu version: ubuntu-22.04, ubuntu-20.04, ubuntu-18.04
ARG VARIANT="jammy"
FROM mcr.microsoft.com/devcontainers/base:${VARIANT}

RUN apt-get update && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get -y install --no-install-recommends wget \
                                               bzip2

# Download and install arm-none-eabi-gcc toolchain

# RUN wget https://developer.arm.com/-/media/Files/downloads/gnu-rm/10.3-2021.10/gcc-arm-none-eabi-10.3-2021.10-x86_64-linux.tar.bz2 -P /home/vscode
# RUN tar xvjf /home/vscode/gcc-arm-none-eabi-10.3-2021.10-x86_64-linux.tar.bz2 -C /usr/share
# RUN ln -s /usr/share/gcc-arm-none-eabi-10.3-2021.10/bin/* /usr/bin/
# RUN rm /home/vscode/gcc-arm-none-eabi-10.3-2021.10-x86_64-linux.tar.bz2

RUN apt-get update && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get -y install --no-install-recommends build-essential \
                                               ninja-build \
                                               git \
                                               python3.11 \
                                               python3-pip \
                                               cpputest \
                                               libncurses5 \
                                               clang-format \
                                               openjdk-19-jdk

RUN pip install meson

# Google Drive file IDs to download
ARG STM32_CLT_INSTALLER_FILE_ID=1EiwKXrybxPzGZKf8njEgnKxl44lq1RFJ
ARG STM32_CUBE_MX_INSTALLER_FILE_ID=1oPy8HTI8QHr0n1vqJy9iJ6M1EMlHL0KU
ARG STM32_CUBE_MX_AUTO_INSTALLER_FILE_ID=1m3WB_VqmxN13ZDQACiD_LrCSMh6JoISB

# Download script
COPY --chown=vscode:vscode --chmod=555 wget_drive.sh /home/vscode/temp/

# Download and instll ST CLT
RUN /home/vscode/temp/wget_drive.sh ${STM32_CLT_INSTALLER_FILE_ID} /home/vscode/temp/stm32clt.zip && \
    unzip /home/vscode/temp/stm32clt.zip -d /home/vscode/temp && \
    chmod 555 /home/vscode/temp/st-stm32cubeclt*.sh && \
    /home/vscode/temp/st-stm32cubeclt*.sh --noexec --keep --target /home/vscode/st/

# USER root

# # Install the required ST CLT packages for debugging and cleanup
# RUN dpkg-deb -x /home/vscode/st/st-stlink-server*.deb / && \
#     dpkg-deb -x /home/vscode/st/st-stm32cubeclt*.deb /  && \
#     rm -r /home/vscode/st

# USER vscode

# Download and install STM32CubeMX
RUN /home/vscode/temp/wget_drive.sh ${STM32_CUBE_MX_INSTALLER_FILE_ID} /home/vscode/temp/stm32cubemx.zip && \
    unzip /home/vscode/temp/stm32cubemx.zip -d /home/vscode/temp && \
    /home/vscode/temp/wget_drive.sh ${STM32_CUBE_MX_AUTO_INSTALLER_FILE_ID} /home/vscode/temp/stm32cubemx_auto-install.xml && \
    /home/vscode/temp/SetupSTM32CubeMX-6.9.2 /home/vscode/temp/stm32cubemx_auto-install.xml

# Clean up downloads
RUN rm -r /home/vscode/temp
