#!/bin/bash

set +e

EDM_LINUX_URL="https://package-data.enthought.com/edm/rh5_x86_64/1.5/edm_1.5.2_linux_x86_64.sh"


download_and_install_edm_mac() {
    brew cask install edm
}

download_and_install_edm_linux() {
    curl -L \
         -o installer.sh \
         "$EDM_LINUX_URL"
    bash installer.sh -b -p "$HOME"
    rm -f installer.sh
    export PATH="$PATH:$HOME/bin"
}

create_environment() {
    edm envs create travisci
    edm install -y -e travisci numpy cython
}


if [ "$(uname)" = "Darwin" ]; then
    download_and_install_edm_mac
else
    download_and_install_edm_linux
fi
create_environment
